import os
import cv2
import numpy as np
import pytesseract
import json
from paddleocr import PaddleOCR
from typing import List, Tuple
from itertools import zip_longest
import requests
from config import api_key, url

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Initialize PaddleOCR
paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# API headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Preprocess the image to improve OCR accuracy.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    return dilate


def extract_text_tesseract(image: np.ndarray) -> Tuple[List[str], List[float], List[Tuple[int, int, int, int]]]:
    """
    Extract text, confidence levels, and bounding boxes using Tesseract.
    """
    ocr_result = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    texts, confidences, boxes = [], [], []
    n_boxes = len(ocr_result['level'])

    for i in range(n_boxes):
        if ocr_result['text'][i].strip() != '':
            texts.append(ocr_result['text'][i])
            confidences.append(float(ocr_result['conf'][i]) / 100)
            (x, y, w, h) = (
            ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][i])
            boxes.append((x, y, w, h))

    return texts, confidences, boxes


def extract_text_paddle(image_path: str) -> Tuple[List[str], List[float], List[Tuple[int, int, int, int]]]:
    """
    Extract text, confidence levels, and bounding boxes using PaddleOCR.
    """
    result = paddle_ocr.ocr(image_path, cls=True)
    texts, confidences, boxes = [], [], []

    for line in result[0]:
        texts.append(line[1][0])  # Extract the recognized text
        confidences.append(float(line[1][1]))  # Confidence score
        boxes.append(line[0])  # The bounding box

    return texts, confidences, boxes


def draw_boxes_on_image(image: np.ndarray, boxes: List[tuple]) -> np.ndarray:
    """
    Draw boxes around the detected text regions on the image.
    PaddleOCR provides quadrilateral boxes, while Tesseract provides rectangular boxes.
    """
    for box in boxes:
        if isinstance(box[0], list) or isinstance(box[0], tuple):  # PaddleOCR gives quadrilateral boxes
            points = np.array(box, dtype=np.int32)
            cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)
        else:  # Tesseract gives rectangular boxes (x, y, w, h)
            x, y, w, h = box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return image


def is_box_overlapping(box1, box2, threshold=0.5):
    """
    Kiểm tra xem hai bounding box có trùng lặp không.
    Sử dụng tỷ lệ trùng lặp (IoU - Intersection over Union) để xác định mức độ trùng lặp.
    """
    x1_min, y1_min, x1_max, y1_max = box1[0][0], box1[0][1], box1[2][0], box1[2][
        1]  # PaddleOCR trả về 4 điểm của hình hộp
    x2_min, y2_min, x2_max, y2_max = box2[0], box2[1], box2[0] + box2[2], box2[1] + box2[
        3]  # Tesseract trả về (x, y, w, h)

    # Tính diện tích của box1 và box2
    area1 = (x1_max - x1_min) * (y1_max - y1_min)
    area2 = (x2_max - x2_min) * (y2_max - y2_min)

    # Tính tọa độ của vùng giao nhau (intersection)
    x_overlap_min = max(x1_min, x2_min)
    y_overlap_min = max(y1_min, y2_min)
    x_overlap_max = min(x1_max, x2_max)
    y_overlap_max = min(y1_max, y2_max)

    # Tính diện tích của vùng giao nhau
    overlap_area = max(0, x_overlap_max - x_overlap_min) * max(0, y_overlap_max - y_overlap_min)

    # Tính tỷ lệ trùng lặp (IoU)
    iou = overlap_area / float(area1 + area2 - overlap_area)

    # Nếu tỷ lệ trùng lặp lớn hơn ngưỡng, coi như trùng lặp
    return iou > threshold

def combine_results(tesseract_data, paddle_data):
    """
    Combine the results from PaddleOCR and Tesseract by merging their texts and boxes,
    with PaddleOCR results appearing first. Tesseract will not detect areas or texts already detected by PaddleOCR.
    """
    paddle_texts, paddle_confidences, paddle_boxes = paddle_data
    tesseract_texts, tesseract_confidences, tesseract_boxes = tesseract_data

    # Kết quả sẽ chứa các kết quả của PaddleOCR
    final_texts = paddle_texts[:]
    final_confidences = paddle_confidences[:]
    final_boxes = paddle_boxes[:]

    # Danh sách để lưu các texts đã phát hiện để tránh trùng lặp
    detected_texts = set(paddle_texts)

    # Lọc bỏ những kết quả trùng lặp từ Tesseract dựa trên texts
    for i, tesseract_text in enumerate(tesseract_texts):
        if tesseract_text.strip() and tesseract_text not in detected_texts:
            # Thêm kết quả từ Tesseract nếu không trùng với PaddleOCR
            final_texts.append(tesseract_text)
            final_confidences.append(tesseract_confidences[i])
            final_boxes.append(tesseract_boxes[i])
            detected_texts.add(tesseract_text)

    return final_texts, final_confidences, final_boxes

# def combine_results(tesseract_data, paddle_data):
#     """
#     Combine the results from PaddleOCR and Tesseract by merging their texts and boxes,
#     with PaddleOCR results appearing first. Tesseract will not detect areas already detected by PaddleOCR.
#     """
#     paddle_texts, paddle_confidences, paddle_boxes = paddle_data
#     tesseract_texts, tesseract_confidences, tesseract_boxes = tesseract_data
#
#     # Kết quả sẽ chứa các kết quả của PaddleOCR
#     final_texts = paddle_texts[:]
#     final_confidences = paddle_confidences[:]
#     final_boxes = paddle_boxes[:]
#
#     # Lọc bỏ những kết quả trùng lặp từ Tesseract
#     for i, tesseract_box in enumerate(tesseract_boxes):
#         overlapping = False
#         for paddle_box in paddle_boxes:
#             if is_box_overlapping(paddle_box, tesseract_box):
#                 overlapping = True
#                 break
#
#         if not overlapping:
#             # Thêm kết quả từ Tesseract nếu không trùng với PaddleOCR
#             final_texts.append(tesseract_texts[i])
#             final_confidences.append(tesseract_confidences[i])
#             final_boxes.append(tesseract_box)
#
#     return final_texts, final_confidences, final_boxes
#

# def combine_results(tesseract_data, paddle_data):
#     """
#     Combine the results from PaddleOCR and Tesseract by merging their texts and boxes,
#     with PaddleOCR results appearing first.
#     """
#     # Kết hợp kết quả từ PaddleOCR trước, sau đó đến Tesseract
#     texts = paddle_data[0] + tesseract_data[0]
#     confidences = paddle_data[1] + tesseract_data[1]
#     boxes = paddle_data[2] + tesseract_data[2]
#
#     return texts, confidences, boxes


def call_nlp_model(prompt: str) -> dict:
    """
    Call the NLP model via the API and return structured JSON data.
    """
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


def process_image(image_path: str, output_image_path: str) -> dict:
    """
    Process an image using both Tesseract and PaddleOCR, and save the output image with drawn boxes.
    """
    # Read and preprocess the image
    image = cv2.imread(image_path)
    preprocessed_image = preprocess_image(image)

    # Extract text and data using both Tesseract and PaddleOCR
    tesseract_data = extract_text_tesseract(preprocessed_image)
    paddle_data = extract_text_paddle(image_path)

    # Combine results from both OCR engines
    texts, confidences, boxes = combine_results(tesseract_data, paddle_data)

    # Draw boxes on the image
    output_image = draw_boxes_on_image(image.copy(), boxes)

    # Save the image with boxes
    cv2.imwrite(output_image_path, output_image)

    # Create a JSON structure
    result = {
        "texts": texts,
        "confidences": confidences
    }

    return result


def remove_duplicates(text: str) -> str:
    """
    Loại bỏ các từ hoặc câu giống nhau trong văn bản.
    """
    # Tách văn bản thành các câu dựa trên dấu chấm câu hoặc dấu xuống dòng
    sentences = text.split()

    # Dùng set để loại bỏ các câu trùng lặp
    unique_sentences = list(dict.fromkeys(sentences))

    # Ghép lại các câu thành một đoạn văn bản duy nhất
    return " ".join(unique_sentences)

def process_image(image_path: str, output_image_path: str) -> dict:
    """
    Process an image using both Tesseract and PaddleOCR, and save the output image with drawn boxes.
    """
    # Read and preprocess the image
    image = cv2.imread(image_path)
    preprocessed_image = preprocess_image(image)

    # Extract text and data using both Tesseract and PaddleOCR
    tesseract_data = extract_text_tesseract(preprocessed_image)
    paddle_data = extract_text_paddle(image_path)

    # Combine results from both OCR engines
    texts, confidences, boxes = combine_results(tesseract_data, paddle_data)

    # Draw boxes on the image
    output_image = draw_boxes_on_image(image.copy(), boxes)

    # Save the image with boxes
    cv2.imwrite(output_image_path, output_image)

    # Join texts into a single string for NLP processing
    extracted_text = " ".join(texts)
    print(extracted_text)
    # Loại bỏ câu hoặc từ trùng lặp
    # extracted_text = remove_duplicates(extracted_text)
    # print(extracted_text)
    # Tạo prompt cho API NLP để xử lý văn bản và lấy thông tin hóa đơn
    prompt = f"""
    Please correct any spelling mistakes in the following text extracted from an image, remove any duplicate entries, and then extract the necessary invoice information.
    Extract the following details:
    - **Corrected Text**: Provide the text after correcting spelling mistakes and removing duplicates.
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

    # Call the NLP model to process the text
    nlp_result = call_nlp_model(prompt)

    # Create a combined result with OCR and NLP analysis
    result = {
        "ocr_data": {
            "texts": texts,
            "confidences": confidences,
            "boxes": boxes
        },
        "nlp_analysis": nlp_result
    }

    return result


def process_images_in_directory(image_dir: str, output_dir: str):
    """
    Process all images in a directory, draw boxes around text, and save output images and JSON files.
    """
    # Define accepted image extensions
    ext = (".jpg", ".jpeg", ".png")

    # Load images from the specified folder
    img_lst: List[str] = [os.path.join(image_dir, item) for item in os.listdir(image_dir) if item.lower().endswith(ext)]

    for img_path in img_lst:
        # Extract the base name of the image file
        img_name = os.path.splitext(os.path.basename(img_path))[0]

        # Define paths for output image and JSON file
        output_image_path = os.path.join(output_dir, f"{img_name}_output.png")
        output_json_path = os.path.join(output_dir, f"{img_name}_output.json")

        # Process the image and extract text and NLP analysis
        data = process_image(img_path, output_image_path)

        # Save extracted text, confidence data, and NLP analysis to a JSON file
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Processed image '{img_name}' saved to '{output_image_path}' and JSON to '{output_json_path}'.")



def main()->None:
    image_dir = 'image11'  # Directory containing images
    output_dir = 'output_images16'  # Directory to save output images and JSON files

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process all images in the directory
    process_images_in_directory(image_dir, output_dir)


if __name__ == '__main__':
    main()