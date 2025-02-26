import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import json
import cv2 as cv
import numpy as np
from typing import List
from paddleocr import PaddleOCR, draw_ocr, PPStructure, save_structure_res, draw_structure_result
from Preprocess import preprocess  # Import preprocess function
from itertools import zip_longest  # For safe unpacking
import requests  # For calling the NLP model
from config import api_key, url, default_prompt_template
from PIL import Image

# Load API key from environment variable
if not api_key:
    raise ValueError("Vui lòng thiết lập biến môi trường API_KEY với API key của bạn.")

# API configurations
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
        except Exception as e:
            print(f"Error in processing NLP response: {e}")
            return {}
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return {}

# Function to use PPStructure to extract tables and structures
def extract_structure(image_path):
    # Khởi tạo PPStructure để nhận diện cấu trúc tài liệu
    table_engine = PPStructure(show_log=True)

    # Đọc ảnh và áp dụng PPStructure
    image = cv.imread(image_path)
    result = table_engine(image)

    # Lưu kết quả nhận diện bảng
    save_folder = 'structure_results'
    os.makedirs(save_folder, exist_ok=True)
    save_structure_res(result, save_folder, image_path.split('/')[-1].split('.')[0])

    # Vẽ kết quả nhận diện và hiển thị
    for i, item in enumerate(result):
        if item['type'] == 'table':
            img = Image.open(image_path).convert('RGB')
            img = draw_structure_result(img, item['res'], item['bbox'])
            img.save(os.path.join(save_folder, f'table_result_{i}.png'))

    return result

def main() -> None:
    # Define output folder for OCR results
    ocr_save_path = "ocr_output11"
    os.makedirs(ocr_save_path, exist_ok=True)

    # Define accepted image extensions
    ext = (".jpg", ".jpeg", ".png")

    # Load images from the "images" folder
    img_dir = "image6"
    img_lst: List[str] = [os.path.join(img_dir, item) for item in os.listdir(img_dir) if item.lower().endswith(ext)]

    if not img_lst:
        print("No images found in the specified directory.")
        return

    # Apply PPStructure to extract tables and structure
    for img_path in img_lst:
        structure_result = extract_structure(img_path)
        print(f"Structure result for {img_path}: {structure_result}")

        # Process OCR for the tables found by PPStructure
        for item in structure_result:
            if item['type'] == 'table':
                # Perform OCR on the extracted table areas
                img_data = cv.imread(img_path)
                paddleOCR = PaddleOCR(lang="en", use_angle_cls=True)
                result = paddleOCR.ocr(img_data, cls=True)

                if result and len(result) > 0 and result[0]:
                    try:
                        # Unpack bounding boxes and text confidences
                        bboxes, text_confs = zip_longest(*result[0], fillvalue=None)
                        texts_confs = [tc if tc is not None else ("", 0.0) for tc in text_confs]
                        texts, confs = zip(*texts_confs)
                        texts = [text if text is not None else "" for text in texts]
                        confs = list(map(float, confs))

                        # Join texts into a single string for NLP processing
                        extracted_text = " ".join(texts)

                        # Tạo prompt cho API NLP để xử lý văn bản và lấy thông tin hóa đơn
                        prompt = default_prompt_template.format(extracted_text=extracted_text)
                        nlp_result = call_nlp_model(prompt)

                        # Save OCR image with bounding boxes and confidence scores
                        ocr_img = draw_ocr(img_data, bboxes, txts=None, scores=confs, drop_score=0.5)
                        ocr_img = cv.cvtColor(ocr_img, cv.COLOR_GRAY2BGR)
                        img_filename = os.path.splitext(os.path.basename(img_path))[0]
                        cv.imwrite(os.path.join(ocr_save_path, f"{img_filename}_ocr.jpg"), ocr_img)

                        # Prepare OCR results for saving
                        ocr_result = {
                            "image_index": img_filename,
                            "texts": texts,
                            "confidences": confs,
                            "bounding_boxes": [bbox.tolist() if isinstance(bbox, np.ndarray) else bbox for bbox in bboxes],
                            "nlp_analysis": nlp_result  # Add NLP result here
                        }

                        # Save each image's OCR results to a separate JSON file
                        json_output_path = os.path.join(ocr_save_path, f"{img_filename}.json")
                        with open(json_output_path, "w", encoding='utf-8') as json_file:
                            json.dump(ocr_result, json_file, indent=4, ensure_ascii=False)

                        # Print out the extracted information in Commercial Invoice format
                        invoice_info = nlp_result.get("invoiceInfo", {})
                        print(f"\nInvoice Information:")
                        print(f"Shipper Company Name: {invoice_info.get('shipperInfo', {}).get('companyName', '')}")
                        print(f"Shipper Address: {invoice_info.get('shipperInfo', {}).get('address', '')}")
                        print(f"Shipper Phone: {invoice_info.get('shipperInfo', {}).get('phoneNumber', '')}")
                        print(f"Consignee Company Name: {invoice_info.get('consigneeInfo', {}).get('companyName', '')}")
                        print(f"Consignee Address: {invoice_info.get('consigneeInfo', {}).get('address', '')}")
                        print(f"Consignee Phone: {invoice_info.get('consigneeInfo', {}).get('phoneNumber', '')}")
                        print(f"Invoice Number: {invoice_info.get('invoiceNumber', '')}")
                        print(f"Invoice Date: {invoice_info.get('invoiceDate', '')}")
                        print(f"Port of Loading: {invoice_info.get('portOfLoading', '')}")
                        print(f"Port of Discharge: {invoice_info.get('portOfDischarge', '')}")
                        print(f"Terms of Payment: {invoice_info.get('termsOfPayment', '')}")
                        print(f"Shipping Method: {invoice_info.get('shippingMethod', '')}")

                    except Exception as e:
                        print(f"Failed to process OCR for table in image {img_filename}: {img_path}. Error: {e}")
            else:
                print(f"No table found in image {img_path}")

if __name__ == '__main__':
    main()
