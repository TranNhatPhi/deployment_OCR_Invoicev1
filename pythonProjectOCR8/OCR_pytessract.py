import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import json
import cv2 as cv
import numpy as np
from typing import List
import pytesseract
from Preprocess import preprocess
from PIL import Image
from itertools import zip_longest  # For safe unpacking
import requests  # For calling the NLP model
from config import api_key, url, default_prompt_template

# Đặt đường dẫn tesseract nếu cần (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Đường dẫn tesseract của bạn

# Load API key từ môi trường
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

def main() -> None:
    # Define output folder for OCR results
    ocr_save_path = "ocr_output24"
    os.makedirs(ocr_save_path, exist_ok=True)

    # Define accepted image extensions
    ext = (".jpg", ".jpeg", ".png")

    # Load images from the "images" folder
    img_dir = "image6"
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
            preprocessed_img,_ = preprocess(img)  # Tiền xử lý ảnh
            img_lst_data.append((img_path, preprocessed_img))  # Lưu cả ảnh gốc và ảnh đã xử lý

    if not img_lst_data:
        print("No valid images to process.")
        return

    # Iterate through the images and apply OCR
    for i, (img_path, preprocessed_img) in enumerate(img_lst_data):
        try:
            # Perform OCR
            extracted_text = pytesseract.image_to_string(preprocessed_img, lang='eng+vie')

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

            # Save OCR image with bounding boxes and confidence scores
            ocr_img = preprocessed_img  # Nếu cần, bạn có thể vẽ bounding box trên ảnh sau khi OCR
            img_filename = os.path.splitext(os.path.basename(img_path))[0]
            cv.imwrite(os.path.join(ocr_save_path, f"{img_filename}_ocr.jpg"), ocr_img)

            # Prepare OCR results for saving
            ocr_result = {
                "image_index": i,
                "extracted_text": extracted_text,
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

            # Invoice Information
            invoice_info = nlp_result.get("invoiceInfo", {})
            print("\nInvoice Information:")
            print(f"Company Name: {invoice_info.get('CompanyName', '')}")
            print(f"Address: {invoice_info.get('address', '')}")
            print(f"Date of Sale: {invoice_info.get('dateOfSale', '')}")
            print(f"Invoice Number: {invoice_info.get('invoiceNumber', '')}")
            print(f"Cashier: {invoice_info.get('cashier', '')}")
            print(f"Table: {invoice_info.get('table', '')}")
            print(f"Customer Type: {invoice_info.get('customerType', '')}")
            print(f"Phone Number: {invoice_info.get('phoneNumber', '')}")
            print(f"Wi-Fi Info: {invoice_info.get('wifiInfo', '')}")
            print(f"Email: {invoice_info.get('email', '')}")
            print(f"Tax ID: {invoice_info.get('taxId', '')}")
            print(f"Invoice Type: {invoice_info.get('invoiceType', '')}")
            print(f"Items Purchased: {invoice_info.get('itemsPurchased', [])}")
            print(f"Total Amount: {invoice_info.get('totalAmount', '')}")
            print(f"Discount: {invoice_info.get('discount', '')}")
            print(f"Payment Method: {invoice_info.get('paymentMethod', '')}")
            print(f"Other Info: {invoice_info.get('otherInfo', [])}")

        except Exception as e:
            print(f"Failed to process OCR for image {i}: {img_path}. Error: {e}")

    return None


if __name__ == '__main__':
    main()
