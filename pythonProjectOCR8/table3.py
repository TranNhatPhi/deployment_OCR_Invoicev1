import os
import cv2 as cv
import numpy as np
from typing import List
from paddleocr import PPStructure, save_structure_res, draw_structure_result
from Preprocess import preprocess  # Import hàm tiền xử lý

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def main() -> None:
    structure_save_path = os.path.join(os.getcwd(), "structure_output1234")
    os.makedirs(structure_save_path, exist_ok=True)
    ext = ("jpg", "jpeg", "png")
    img_lst: List[str] = [os.path.join(os.getcwd(), "images", item) for item in os.listdir(
        os.path.join(os.getcwd(), "images")) if item.endswith(ext)]

    # Đường dẫn đến tệp phông chữ (.ttf)
    font_path = "C:/Windows/Fonts/arial.ttf"  # Chỉnh sửa đường dẫn này nếu cần

    ppStructure = PPStructure(
            lang="en",                # Ngôn ngữ OCR, ví dụ: "en" cho tiếng Anh
            show_log=False,           # Hiển thị log (False để tắt log)
            layout=True,              # Bật mô hình nhận diện bố cục tài liệu (ví dụ: bảng, hình ảnh, đoạn văn)
            table=True,               # Bật mô hình nhận diện bảng
        )

    for i, img_path in enumerate(img_lst):
        # Đọc ảnh gốc
        imgOriginal = cv.imread(img_path, cv.IMREAD_UNCHANGED)

        # Tiền xử lý ảnh để tăng cường chất lượng
        imgGrayscale, imgThresh = preprocess(imgOriginal)

        # Chuyển ảnh đã tiền xử lý từ Grayscale về RGB để phù hợp với PaddleOCR
        imgForOcr = cv.cvtColor(imgThresh, cv.COLOR_GRAY2RGB)

        # Kết quả phân tích cấu trúc từ ảnh đã tiền xử lý
        analyzed_structures = ppStructure(imgForOcr)

        # Lưu kết quả đã phát hiện
        save_structure_res(res=analyzed_structures,
                           save_folder=structure_save_path, img_name=str(i))

        # Vẽ bounding box lên ảnh sử dụng PaddleOCR draw function
        draw_img = draw_structure_result(imgForOcr, analyzed_structures, font_path)

        # Lưu ảnh đã vẽ
        cv.imwrite(os.path.join(structure_save_path, f"{i}.jpg"), cv.cvtColor(draw_img, cv.COLOR_RGB2BGR))

    return None


if __name__ == '__main__':
    main()
