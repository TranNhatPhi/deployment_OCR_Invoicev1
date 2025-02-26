from pdf2image import convert_from_path, pdfinfo_from_path
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Đường dẫn đến tệp PDF
pdf_path = 'NKC_T01_15.pdf'

# Thư mục để lưu trữ các hình ảnh
output_folder = 'image6'
os.makedirs(output_folder, exist_ok=True)

# Check if poppler is` accessible
pdfinfo_from_path(pdf_path)

# Chuyển đổi PDF sang hình ảnh
images = convert_from_path(pdf_path)
# Lưu các hình ảnh vào thư mục
for i, image in enumerate(images):
    image_path = os.path.join(output_folder, f'page_{i + 1}.PNG')
    image.save(image_path, 'PNG')


