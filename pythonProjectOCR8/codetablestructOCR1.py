import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import subprocess

# Chạy lệnh nhận diện bảng
subprocess.run(['python', 'PaddleOCR/ppstructure/table/predict_table.py',
                '--det_model_dir=inference/en_PP-OCRv3_det_infer',
                '--rec_model_dir=inference/en_ppocr_mobile_v2.0_table_rec_infer',
                '--table_model_dir=inference/en_ppocr_mobile_v2.0_table_structure_infer',
                '--image_dir=images/1.jpg',
                '--rec_char_dict_path=../ppocr/utils/dict/table_dict.txt',
                '--table_char_dict_path=../ppocr/utils/dict/table_structure_dict.txt',
                '--det_limit_side_len=736',
                '--det_limit_type=min',
                '--output=./output/table1'])

# Giả sử bạn đã nhận được kết quả từ OCR
ocr_result = "Kết quả từ OCR sau khi nhận diện bảng"

# Lưu kết quả ra file text
output_file_path = 'D:/savecode/pythonProjectOCR8/output/ocr_result.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(ocr_result)

print(f"Kết quả đã được lưu vào {output_file_path}")
