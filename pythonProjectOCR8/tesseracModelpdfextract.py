import cv2
import numpy as np
import pytesseract
import json
import os
from paddleocr import PaddleOCR
from typing import List, Tuple
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Initialize PaddleOCR
paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


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


def combine_results(tesseract_data, paddle_data):
    """
    Combine the results from Tesseract and PaddleOCR by merging their texts and boxes.
    """
    texts = tesseract_data[0] + paddle_data[0]
    confidences = tesseract_data[1] + paddle_data[1]
    boxes = tesseract_data[2] + paddle_data[2]

    return texts, confidences, boxes


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

        # Process the image and extract text
        data = process_image(img_path, output_image_path)

        # Save extracted text and confidence data to a JSON file
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Processed image '{img_name}' saved to '{output_image_path}' and JSON to '{output_json_path}'.")


# Example usage
image_dir = 'imagess1'  # Directory containing images
output_dir = 'output_images113131'  # Directory to save output images and JSON files

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process images in the directory
process_images_in_directory(image_dir, output_dir)
