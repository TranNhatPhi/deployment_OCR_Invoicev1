import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import cv2 as cv
import pytesseract
import numpy as np
import json
from typing import List
from itertools import zip_longest  # For safe unpacking
import requests  # For calling the NLP model
from config import api_key, url, default_prompt_template

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
        "temperature": 0.5
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


def draw_ocr_boxes(img_data, ocr_result):
    """
    Vẽ bounding boxes và văn bản lên ảnh.

    Args:
        img_data: Hình ảnh đã đọc.
        ocr_result: Kết quả OCR chứa thông tin bounding boxes và văn bản.

    Returns:
        img_with_boxes: Hình ảnh với các bounding boxes và văn bản đã vẽ.
    """
    img_with_boxes = img_data.copy()

    # Lấy các bounding boxes và văn bản từ kết quả OCR
    for box, text in ocr_result:
        # Vẽ bounding box
        points = np.array(box, dtype=np.int32)
        points = points.reshape((-1, 1, 2))
        cv.polylines(img_with_boxes, [points], isClosed=True, color=(0, 0, 255), thickness=2)

        # Vẽ văn bản lên ảnh
        x, y = box[0]  # Lấy tọa độ của góc trên bên trái
        cv.putText(img_with_boxes, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return img_with_boxes


def main() -> None:
    # Define output folder for OCR results
    ocr_save_path = "ocr_output"
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
            img_lst_data.append(img)

    if not img_lst_data:
        print("No valid images to process.")
        return

    # Iterate through the images and apply OCR using Tesseract
    for i, img_path in enumerate(img_lst):
        img_data = img_lst_data[i]

        # Apply Tesseract OCR
        ocr_result = pytesseract.image_to_data(img_data, output_type=pytesseract.Output.DICT)

        # Prepare bounding boxes and text
        boxes = []
        texts = []
        for i in range(len(ocr_result['text'])):
            text = ocr_result['text'][i]
            if text.strip() != "":  # Kiểm tra văn bản không rỗng
                x, y, w, h = ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][
                    i]
                boxes.append([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])  # Lưu các điểm góc của bounding box
                texts.append(text)

        ocr_result = list(zip(boxes, texts))

        # Vẽ bounding boxes và văn bản lên ảnh
        img_with_boxes = draw_ocr_boxes(img_data, ocr_result)

        # Save OCR image with bounding boxes
        img_filename = os.path.splitext(os.path.basename(img_path))[0]
        cv.imwrite(os.path.join(ocr_save_path, f"{img_filename}_ocr.jpg"), img_with_boxes)

        # Join texts into a single string for NLP processing
        extracted_text = " ".join(texts)

        # Create prompt for NLP API to process the extracted text
        prompt = f"""
            Please extract the necessary commercial invoice information from the following text:
            Extract the following details:
            - Shipper Information:
              - Company Name
              - Address
              - Phone Number
            - Consignee Information:
              - Company Name
              - Address
              - Phone Number
            - Invoice Number
            - Invoice Date
            - Port of Loading
            - Port of Discharge
            - Terms of Payment
            - Shipping Method
            - Items Purchased (name, quantity, unit price, total price)
            - Total Amount
            - Gross Weight
            - Net Weight

            Provide the output in the following JSON format:

            {{
                "shipperInfo": {{
                    "companyName": "",
                    "address": "",
                    "phoneNumber": ""
                }},
                "consigneeInfo": {{
                    "companyName": "",
                    "address": "",
                    "phoneNumber": ""
                }},
                "invoiceNumber": "",
                "invoiceDate": "",
                "portOfLoading": "",
                "portOfDischarge": "",
                "termsOfPayment": "",
                "shippingMethod": "",
                "itemsPurchased": [
                    {{
                        "name": "",
                        "quantity": "",
                        "unitPrice": "",
                        "totalPrice": ""
                    }}
                ],
                "totalAmount": "",
                "grossWeight": "",
                "netWeight": ""
            }}

            Here is the extracted text:
            \"\"\" 
            {extracted_text}
            \"\"\" 
        """

        # Call the NLP model
        nlp_result = call_nlp_model(prompt)

        # Prepare OCR results for saving
        ocr_result_data = {
            "image_index": i,
            "texts": texts,
            "bounding_boxes": [bbox.tolist() if isinstance(bbox, np.ndarray) else bbox for bbox in boxes],
            "nlp_analysis": nlp_result  # Add NLP result here
        }

        # Save each image's OCR results to a separate JSON file
        json_output_path = os.path.join(ocr_save_path, f"{img_filename}.json")
        with open(json_output_path, "w", encoding='utf-8') as json_file:
            json.dump(ocr_result_data, json_file, indent=4, ensure_ascii=False)

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

        # In danh sách các mặt hàng đã mua
        print("\nItems Purchased:")
        for item in invoice_info.get('itemsPurchased', []):
            print(
                f"- {item.get('name', '')} | Quantity: {item.get('quantity', '')} | Unit Price: {item.get('unitPrice', '')} | Total Price: {item.get('totalPrice', '')}")

        print(f"Total Amount: {invoice_info.get('totalAmount', '')}")
        print(f"Gross Weight: {invoice_info.get('grossWeight', '')}")
        print(f"Net Weight: {invoice_info.get('netWeight', '')}")


if __name__ == '__main__':
    main()
