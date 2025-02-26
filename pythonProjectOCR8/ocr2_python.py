# OCR_RECO.py

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import json
import cv2 as cv
import numpy as np
from typing import List
from paddleocr import PaddleOCR, draw_ocr
from Preprocess import preprocess  # Import preprocess function
from itertools import zip_longest  # For safe unpacking
import requests  # For calling the NLP model

# Load API key from environment variable
api_key = "sk-VXgtH6RV1IbN3Q072b5bD03aCfD84bAaBd92458e9a3c6303"
if not api_key:
    raise ValueError("Vui lòng thiết lập biến môi trường API_KEY với API key của bạn.")

# API configurations
url = "https://yescale.one/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Function to call the NLP model via the API and return structured JSON data
def call_nlp_model(prompt: str) -> dict:
    global reply_content
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000,
        "temperature": 1
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            reply_content = response.json()['choices'][0]['message']['content']
            # Attempt to parse the JSON content
            json_start = reply_content.find('{')
            json_end = reply_content.rfind('}') + 1
            json_str = reply_content[json_start:json_end]
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print("Model response:", reply_content)
            return {}
        except Exception as e:
            print(f"Error in processing NLP response: {e}")
            return {}
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return {}

def main() -> None:
    # Define output folder for OCR results
    ocr_save_path = "ocr_output1"
    os.makedirs(ocr_save_path, exist_ok=True)

    # Define accepted image extensions
    ext = (".jpg", ".jpeg", ".png")

    # Load images from the "images" folder
    img_dir = "image3"
    img_lst: List[str] = [os.path.join(img_dir, item) for item in os.listdir(img_dir) if item.lower().endswith(ext)]

    if not img_lst:
        print("No images found in the specified directory.")
        return

    # Load and preprocess images
    img_lst_data: List[np.ndarray] = []
    for img_path in img_lst:
        img = cv.imread(img_path, cv.IMREAD_COLOR)
        if img is None:
            print(f"Failed to load image: {img_path}")
        else:
            img_lst_data.append(img)

    if not img_lst_data:
        print("No valid images to process.")
        return

    # Apply preprocessing to each image
    preprocessed_images = []
    for img in img_lst_data:
        try:
            _, preprocessed_img = preprocess(img)  # Preprocess and take the thresholded image
            preprocessed_images.append(preprocessed_img)
        except Exception as e:
            print(f"Preprocessing failed: {e}")

    # Initialize PaddleOCR
    paddleOCR = PaddleOCR(
        lang="en",
        use_angle_cls=True,
        show_log=False,
        det_db_thresh=0.5,
        det_db_unclip_ratio=1.7,
        drop_score=0.1,
        max_batch_size=2,
        gpu_mem=2000,
        total_process_num=8
    )

    # Iterate through the images and apply OCR
    for i, img_path in enumerate(img_lst):
        img_data = preprocessed_images[i]

        # Perform OCR
        result = paddleOCR.ocr(img_data)

        if result and len(result) > 0 and result[0]:
            # Unpack bounding boxes and text confidences, handle potential length mismatch
            try:
                bboxes, text_confs = zip_longest(*result[0], fillvalue=None)
                texts_confs = [tc if tc is not None else ("", 0.0) for tc in text_confs]
                texts, confs = zip(*texts_confs)
                texts = [text if text is not None else "" for text in texts]
                confs = list(map(float, confs))

                # Join texts into a single string for NLP processing
                extracted_text = " ".join(texts)

                # Build prompt for NLP model
                prompt = f"""
Please correct any spelling mistakes in the following text extracted from an image, and then extract the necessary invoice information.

Extract the following details:

- **Corrected Text**: Provide the text after correcting spelling mistakes.

- **Invoice Information**:
  - Company Name
  - Address
  - Date of Sale (Ngay ban)
  - Invoice Number (Hoa don so)
  - Cashier (Thu ngan)
  - Table (Ban)
  - Customer Type (Khach hang than thiet)
  - Phone Number (SDT or Dien thoai)
  - Wi-Fi Information (e.g., Wi-Fi name and password)
  - Items Purchased (list of items with name, quantity, unit price, total price)
  - Total Amount (Tong cong)
  - Discount (Chiet khau)
  - Payment Method (Thanh toan)
  - Any other relevant information

Provide the output in JSON format as per the structure:

{{
    "correctedText": "",
    "invoiceInfo": {{
        "CompanyName": "",
        "address": "",
        "dateOfSale": "",
        "invoiceNumber": "",
        "cashier": "",
        "table": "",
        "customerType": "",
        "phoneNumber": "",
        "wifiInfo": "",
        "itemsPurchased": [],
        "totalAmount": "",
        "discount": "",
        "paymentMethod": "",
        "otherInfo": []
    }}
}}

Here is the extracted text:
\"\"\"
{extracted_text}
\"\"\"
"""

                # Call the NLP model
                nlp_result = call_nlp_model(prompt)

                # Save OCR image with bounding boxes and confidence scores
                ocr_img = draw_ocr(
                    img_data, bboxes, txts=None, scores=confs, drop_score=0.5)
                ocr_img = cv.cvtColor(ocr_img, cv.COLOR_GRAY2BGR)
                img_filename = os.path.splitext(os.path.basename(img_path))[0]
                cv.imwrite(os.path.join(ocr_save_path, f"{img_filename}_ocr.jpg"), ocr_img)

                # Prepare OCR results for saving
                ocr_result = {
                    "image_index": i,
                    "texts": texts,
                    "confidences": confs,
                    "bounding_boxes": [bbox.tolist() if isinstance(bbox, np.ndarray) else bbox for bbox in bboxes],
                    "nlp_analysis": nlp_result  # Add NLP result here
                }

                # Save each image's OCR results to a separate JSON file
                json_output_path = os.path.join(ocr_save_path, f"{img_filename}.json")
                with open(json_output_path, "w", encoding='utf-8') as json_file:
                    json.dump(ocr_result, json_file, indent=4, ensure_ascii=False)

                # Print out the extracted information
                print(f"Processed image {i}: {img_filename}")
                print("\nCorrected Text:")
                print(nlp_result.get("correctedText", ""))
                print("\nInvoice Information:")
                print(nlp_result.get("invoiceInfo", {}))
            except Exception as e:
                print(f"Failed to process OCR for image {i}: {img_path}. Error: {e}")
        else:
            print(f"No text found for image {i}: {os.path.basename(img_path)}")

    return None


if __name__ == '__main__':
    main()
