import os
import json
import cv2
import numpy as np
from paddleocr import PaddleOCR, PPStructure, draw_ocr, save_structure_res
from Preprocess import preprocess  # Import preprocess function
from itertools import zip_longest
import requests
from config import api_key, url, default_prompt_template

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# API configuration
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


# Function to run PPStructure on an image
def run_ppstructure_on_image(image_path, imgThresh):
    # Khởi tạo đối tượng PPStructure
    pp_structure = PPStructure(
        det_db_thresh=0.5,
        det_db_unclip_ratio=1.7,
        drop_score=0.01
    )

    # Gọi phương thức __call__ để phát hiện trên hình ảnh sau khi tiền xử lý
    result = pp_structure(imgThresh)

    # Xử lý và hiển thị kết quả
    img = cv2.imread(image_path)  # Đọc lại ảnh gốc để vẽ lên ảnh gốc
    for res in result:
        if res['type'] == 'text':  # Chỉ lấy phần text
            bbox = res['bbox']
            text = res['res']

            # Vẽ bounding box lên hình ảnh gốc
            cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)

            # Hiển thị text lên hình ảnh tại vị trí bounding box
            cv2.putText(img, text[0]['text'], (int(bbox[0]), int(bbox[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 255, 0), 2)

    # Lưu ảnh đã được vẽ kết quả
    output_image_path = os.path.splitext(image_path)[0] + "_ppstructure_result.jpg"
    cv2.imwrite(output_image_path, img)
    print(f"Saved PPStructure result image: {output_image_path}")


# Function to run the full process (OCR + PPStructure + NLP)
def main():
    # Thư mục chứa các ảnh cần xử lý
    img_dir = "images1"

    # Lấy danh sách các ảnh trong thư mục
    ext = (".jpg", ".jpeg", ".png")
    img_lst = [os.path.join(img_dir, img_name) for img_name in os.listdir(img_dir) if img_name.lower().endswith(ext)]

    if not img_lst:
        print(f"No images found in directory: {img_dir}")
        return

    # Khởi tạo PaddleOCR
    paddleOCR = PaddleOCR(
        lang="en",
        use_angle_cls=True,
        show_log=True,
        det_db_thresh=0.1,
        det_db_unclip_ratio=2.3,
        drop_score=0.01,
        max_batch_size=1,
        gpu_mem=1000,
        total_process_num=8,
        use_cuda=True,
        use_gpu=True
    )

    # Lặp qua danh sách các ảnh
    for img_path in img_lst:
        print(f"Processing image: {img_path}")

        # Đọc và tiền xử lý ảnh
        img = cv2.imread(img_path)
        if img is None or img.size == 0:
            print(f"Failed to load image: {img_path}")
            continue

        # Áp dụng tiền xử lý
        imgGrayscale, imgThresh = preprocess(img)

        # Perform OCR
        result = paddleOCR.ocr(imgThresh, cls=True)

        if result and len(result) > 0 and result[0]:
            try:
                bboxes, text_confs = zip_longest(*result[0], fillvalue=None)
                texts_confs = [tc if tc is not None else ("", 0.0) for tc in text_confs]
                texts, confs = zip(*texts_confs)
                texts = [text if text is not None else "" for text in texts]
                confs = list(map(float, confs))

                # Join texts into a single string for NLP processing
                extracted_text = " ".join(texts)

                # Tạo prompt cho API NLP để xử lý văn bản và lấy thông tin hóa đơn
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
                # Call the NLP model
                nlp_result = call_nlp_model(prompt)

                # Print out the extracted information
                print("\nCorrected Text:")
                print(nlp_result.get("correctedText", ""))

                # Invoice Information
                invoice_info = nlp_result.get("invoiceInfo", {})
                print("\nInvoice Information:")
                for key, value in invoice_info.items():
                    print(f"{key}: {value}")

                # Lưu ảnh OCR
                ocr_img = draw_ocr(img, bboxes, txts=None, scores=confs, drop_score=0.5)
                ocr_img = cv2.cvtColor(ocr_img, cv2.COLOR_GRAY2BGR)
                ocr_output_image_path = os.path.splitext(img_path)[0] + "_ocr_result.jpg"
                cv2.imwrite(ocr_output_image_path, ocr_img)
                print(f"Saved OCR result image: {ocr_output_image_path}")

            except Exception as e:
                print(f"Failed to process OCR for image: {img_path}. Error: {e}")

        # Chạy PPStructure trên ảnh sau khi tiền xử lý
        run_ppstructure_on_image(img_path, imgThresh)


if __name__ == '__main__':
    main()
