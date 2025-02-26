import os
import json
import cv2 as cv
import numpy as np
from typing import List
from paddleocr import PaddleOCR, draw_ocr, PPStructure, draw_structure_result
from itertools import zip_longest
import requests
from config import api_key, url

# Set environment variables
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Đường dẫn tới tệp phông chữ, kiểm tra và thay đổi nếu cần
font_path = "E:/dejavu-fonts-ttf-2.37/dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf"  # Đảm bảo đường dẫn này chính xác

# Kiểm tra xem phông chữ có tồn tại không
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found at path: {font_path}. Please check the font path.")

# Load API key from environment variable
if not api_key:
    raise ValueError("Vui lòng thiết lập biến môi trường API_KEY với API key của bạn.")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Function to call the NLP model via the API and return structured JSON data
def call_nlp_model(prompt: str) -> dict:
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000,
        "temperature": 0.9
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        try:
            reply_content = response.json()['choices'][0]['message']['content']
            json_start = reply_content.find('{')
            json_end = reply_content.rfind('}') + 1
            json_str = reply_content[json_start:json_end]
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print("Model response:", reply_content)
            return {}
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return {}

# Hàm chuyển đổi tất cả mảng ndarray thành danh sách cho cấu trúc bảng
def convert_structure_result_to_serializable(structure_result):
    for item in structure_result:
        for key, value in item.items():
            if isinstance(value, np.ndarray):
                item[key] = value.tolist()  # Chuyển ndarray thành danh sách
            elif isinstance(value, list):
                item[key] = [v.tolist() if isinstance(v, np.ndarray) else v for v in value]
    return structure_result

def main() -> None:
    # Define output folder for OCR results
    ocr_save_path = "ocr_output_combined11"
    os.makedirs(ocr_save_path, exist_ok=True)

    # Define accepted image extensions
    ext = (".jpg", ".jpeg", ".png")

    # Load images from the "images" folder
    img_dir = "image11"
    img_lst: List[str] = [os.path.join(img_dir, item) for item in os.listdir(img_dir) if item.lower().endswith(ext)]

    if not img_lst:
        print("No images found in the specified directory.")
        return

    # Initialize PaddleOCR and PPStructure for table detection
    paddleOCR = PaddleOCR(
        lang="en",
        use_angle_cls=True,
        det=True,
        rec=True,
        show_log=True,
    )
    table_engine = PPStructure(show_log=True)

    # Iterate through the images and apply OCR
    for i, img_path in enumerate(img_lst):
        img = cv.imread(img_path, cv.IMREAD_COLOR)

        if img is None:
            print(f"Failed to load image: {img_path}")
            continue

        # Perform OCR on the image
        result = paddleOCR.ocr(img, cls=True)

        # Perform table structure detection
        structure_result = table_engine(img)

        # Chuyển đổi các kết quả cấu trúc bảng thành JSON serializable (chuyển ndarray thành list)
        structure_result = convert_structure_result_to_serializable(structure_result)

        # Process OCR result if available
        if result and len(result) > 0 and result[0]:
            try:
                bboxes, text_confs = zip_longest(*result[0], fillvalue=None)
                texts_confs = [tc if tc is not None else ("", 0.0) for tc in text_confs]
                texts, confs = zip(*texts_confs)
                texts = [text if text is not None else "" for text in texts]
                confs = list(map(float, confs))

                # Convert bounding boxes from ndarray to list for JSON serialization
                bboxes = [bbox.tolist() if isinstance(bbox, np.ndarray) else bbox for bbox in bboxes]

                # Join texts into a single string for NLP processing
                extracted_text = " ".join(texts)

                # Create prompt for the NLP API
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
                  - Email
                  - Tax ID (Ma so thue)
                  - Invoice Type (Loai hoa don)
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
                        "email": "",
                        "taxId": "",
                        "invoiceType": "",
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
                nlp_result = call_nlp_model(prompt)

                # Draw OCR results on the image
                ocr_img = draw_ocr(img, bboxes, txts=texts, scores=confs)
                ocr_img = cv.cvtColor(ocr_img, cv.COLOR_BGR2RGB)

                # Save OCR image with bounding boxes and confidence scores
                img_filename = os.path.splitext(os.path.basename(img_path))[0]
                cv.imwrite(os.path.join(ocr_save_path, f"{img_filename}_ocr.jpg"), ocr_img)

                # Draw table structure results (use font_path here)
                structure_img = draw_structure_result(img, structure_result, font_path=font_path)
                cv.imwrite(os.path.join(ocr_save_path, f"{img_filename}_structure.jpg"), structure_img)

                # Save OCR and table structure results to JSON
                ocr_result = {
                    "image_index": i,
                    "texts": texts,
                    "confidences": confs,
                    "bounding_boxes": bboxes,  # Now it can be serialized to JSON
                    "nlp_analysis": nlp_result,
                    "table_structure": structure_result  # Đã chuyển thành serializable
                }

                json_output_path = os.path.join(ocr_save_path, f"{img_filename}.json")
                with open(json_output_path, "w", encoding='utf-8') as json_file:
                    json.dump(ocr_result, json_file, indent=4, ensure_ascii=False)

                # Print extracted information
                print(f"Processed image {i}: {img_filename}")
                print(f"OCR result saved to {json_output_path}")

            except Exception as e:
                print(f"Failed to process OCR for image {i}: {img_path}. Error: {e}")
        else:
            print(f"No text found for image {i}: {os.path.basename(img_path)}")

if __name__ == '__main__':
    main()
