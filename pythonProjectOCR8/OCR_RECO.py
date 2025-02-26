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


def main() -> None:
    # Define output folder for OCR results
    ocr_save_path = "ocr_output1"
    os.makedirs(ocr_save_path, exist_ok=True)

    # Define accepted image extensions
    ext = ("jpg", "jpeg", "png")

    # Load images from the "images" folder
    img_dir = "images2"
    img_lst: List[str] = [os.path.join(img_dir, item) for item in os.listdir(img_dir) if item.endswith(ext)]

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
    paddleOCR = PaddleOCR( lang="en",  # English language model
    use_angle_cls=True,  # Enable angle classification for rotated text
    show_log=True,  # Disable detailed logging for better performance
    det_db_thresh=0.5,  # Higher sensitivity for detecting text
    det_db_unclip_ratio=1.7,  # Adjust bounding box size for better text capture
    drop_score=0.1,  # Filter out low-confidence text recognition results
    max_batch_size=0.3,  # Use smaller batch size to avoid memory issues
    gpu_mem=1000,  # Increase GPU memory limit for better performance
    total_process_num=8,  # Use 8 subprocesses for better resource management
    use_cuda = True,
    use_gpu = True
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
                texts, confs = zip(*text_confs)
                texts = list(texts)
                confs = list(map(float, confs))

                # Save OCR image with bounding boxes and confidence scores
                ocr_img = draw_ocr(
                    img_data, bboxes, txts=None, scores=confs, drop_score=0.5)
                ocr_img = cv.cvtColor(ocr_img, cv.COLOR_GRAY2BGR)
                cv.imwrite(os.path.join(ocr_save_path, f"{i}.jpg"), ocr_img)

                # Prepare OCR results for saving
                ocr_result = {
                    "image_index": i,
                    "texts": texts,
                    "confidences": confs,
                    "bounding_boxes": bboxes
                }

                # Save each image's OCR results to a separate JSON file
                img_filename = os.path.splitext(os.path.basename(img_path))[0]
                json_output_path = os.path.join(ocr_save_path, f"{img_filename}.json")
                with open(json_output_path, "w") as json_file:
                    json.dump(ocr_result, json_file, indent=4)

                print(f"Processed image {i}: {img_filename}")
                print("\n")
                print(texts)
            except Exception as e:
                print(f"Failed to process OCR for image {i}: {img_path}. Error: {e}")
        else:
            print(f"No text found for image {i}: {os.path.basename(img_path)}")

    return None


if __name__ == '__main__':
    main()
