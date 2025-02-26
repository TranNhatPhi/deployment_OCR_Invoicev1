import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import requests
import tarfile

# Hàm tải file bằng requests
# def download_file(url, output_path):
#     response = requests.get(url, stream=True)
#     with open(output_path, 'wb') as file:
#         for chunk in response.iter_content(chunk_size=1024):
#             if chunk:
#                 file.write(chunk)
#
# # Tạo thư mục inference nếu chưa có
# if not os.path.exists('inference'):
#     os.mkdir('inference')
#
# # Di chuyển vào thư mục inference
# os.chdir('inference')

# # Tải các file mô hình
# print("Tải mô hình phát hiện bảng...")
# download_file('https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar', 'en_PP-OCRv3_det_infer.tar')
# # Tải các file mô hình
# print("Tải mô hình phát hiện bảng...")
# download_file('https://paddleocr.bj.bcebos.com/dygraph_v2.0/table/en_ppocr_mobile_v2.0_table_det_infer.tar', 'en_ppocr_mobile_v2.0_table_det_infer.tar')

# print("Tải mô hình nhận dạng bảng...")
# download_file('https://paddleocr.bj.bcebos.com/dygraph_v2.0/table/en_ppocr_mobile_v2.0_table_rec_infer.tar', 'en_ppocr_mobile_v2.0_table_rec_infer.tar')
#
# print("Tải mô hình cấu trúc bảng...")
# download_file('https://paddleocr.bj.bcebos.com/dygraph_v2.0/table/en_ppocr_mobile_v2.0_table_structure_infer.tar', 'en_ppocr_mobile_v2.0_table_structure_infer.tar')
#
# Giải nén các file tar
# def extract_tar_file(tar_path, extract_path):
#     with tarfile.open(tar_path) as tar:
#         tar.extractall(path=extract_path)

# print("Giải nén mô hình phát hiện bảng...")
# extract_tar_file('en_ppocr_mobile_v2.0_table_det_infer.tar', './')
#
# print("Giải nén mô hình nhận dạng bảng...")
# extract_tar_file('en_ppocr_mobile_v2.0_table_rec_infer.tar', './')
#
# print("Giải nén mô hình cấu trúc bảng...")
# extract_tar_file('en_ppocr_mobile_v2.0_table_structure_infer.tar', './')
#
# print("Giải nén mô hình cấu trúc bảng...")
# extract_tar_file('en_PP-OCRv3_det_infer.tar', './')
# print("Hoàn tất!")
#
os.system('python PaddleOCR/ppstructure/table/predict_table.py --det_model_dir=inference/en_PP-OCRv3_det_infer \
    --rec_model_dir=inference/en_ppocr_mobile_v2.0_table_rec_infer \
    --table_model_dir=inference/en_ppocr_mobile_v2.0_table_structure_infer \
    --image_dir=images/1.jpg \
    --rec_char_dict_path=PaddleOCR/ppocr/utils/dict/table_dict.txt \
    --table_char_dict_path=PaddleOCR/ppocr/utils/dict/table_structure_dict.txt \
    --det_limit_side_len=736 \
    --det_limit_type=min \
    --output ./output/table1 \
    --draw_img_save_dir=output/det_image')
# os.system('python PaddleOCR/tools/infer/predict_system.py --det_model_dir=inference/en_PP-OCRv3_det_infer \
#     --rec_model_dir=inference/en_PP-OCRv3_rec_infer \
#     --image_dir=images/1.jpg \
#     --rec_char_dict_path=PaddleOCR/ppocr/utils/ppocr_keys_v1.txt \
#     --draw_img_save_dir=output/det_image')

