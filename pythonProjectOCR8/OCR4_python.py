from flask import Flask, jsonify, request,send_from_directory
import time

from flask_cors import CORS
import os
import pandas as pd

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import json
import cv2 as cv
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
import mysql.connector
from itertools import zip_longest
import requests
from Preprocess import preprocess  # Im port preprocess function từ module Preprocess
from config import api_key, url, default_prompt_template
from werkzeug.utils import secure_filename
import aiomysql
import asyncio
from aiohttp import ClientSession
if not api_key or not url:
    raise ValueError("Vui lòng thiết lập biến môi trường API_KEY và API_URL với API key và URL của bạn.")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# # Cấu hình kết nối MySQL
async def get_db_connection():
    return await aiomysql.connect(
        host='localhost',
        port=3307,
        user='root',
        password='123456',
        db='myapp',
        loop=asyncio.get_event_loop()
    )


#########################GET########################################################
@app.route('/api/get_data', methods=['GET'])
async def get_all_data():
    conn = await get_db_connection()  # Use async connection
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        query = "SELECT * FROM invoices ORDER BY image_index DESC"
        await cursor.execute(query)
        rows = await cursor.fetchall()

    conn.close()

    return jsonify(rows)


@app.route('/api/get_data/<int:image_index>', methods=['GET'])
def get_data_by_index(image_index):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM invoices WHERE image_index = %s"
    cursor.execute(query, (image_index,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return jsonify(row)
    else:
        return jsonify({'error': 'Data not found'}), 404


@app.route('/api/get_texts', methods=['GET'])
def get_texts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT image_index, texts, corrected_text FROM invoices"
    cursor.execute(query)
    rows = cursor.fetchall()

    texts = [row['texts'] for row in rows]
    corrected_texts = [row['corrected_text'] for row in rows]

    cursor.close()
    conn.close()

    return jsonify({'texts': texts, 'correctedTexts': corrected_texts})


@app.route('/api/get_texts/<int:image_index>', methods=['GET'])
def get_texts_by_index(image_index):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT texts, corrected_text FROM invoices WHERE image_index = %s"
    cursor.execute(query, (image_index,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return jsonify({
            'image_index': image_index,
            'texts': row['texts'],
            'correctedText': row['corrected_text']
        })
    else:
        return jsonify({'error': 'Texts not found for image_index {}'.format(image_index)}), 404


@app.route('/api/get_invoice_info', methods=['GET'])
def get_invoice_info():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM invoices"
    cursor.execute(query)
    rows = cursor.fetchall()

    invoice_info_list = []
    for row in rows:
        invoice_info_list.append({
            'image_index': row['image_index'],
            'correctedText': row['corrected_text'],
            'invoiceInfo': {
                'companyName': row['company_name'],
                'address': row['address'],
                'dateOfSale': row['date_of_sale'],
                'invoiceNumber': row['invoice_number'],
                'cashier': row['cashier'],
                'table': row['table_info'],
                'customerType': row['customer_type'],
                'phoneNumber': row['phone_number'],
                'wifiInfo': row['wifi_info'],
                'totalAmount': row['total_amount'],
                'discount': row['discount'],
                'paymentMethod': row['payment_method'],
                'itemsPurchased': json.loads(row['items_purchased']) if row['items_purchased'] else []
            }
        })

    cursor.close()
    conn.close()

    return jsonify(invoice_info_list)


@app.route('/api/get_invoice_info/<int:image_index>', methods=['GET'])
def get_invoice_info_by_index(image_index):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM invoices WHERE image_index = %s"
    cursor.execute(query, (image_index,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return jsonify({
            'image_index': image_index,
            'correctedText': row['corrected_text'],
            'invoiceInfo': {
                'companyName': row['company_name'],
                'address': row['address'],
                'dateOfSale': row['date_of_sale'],
                'invoiceNumber': row['invoice_number'],
                'cashier': row['cashier'],
                'table': row['table_info'],
                'customerType': row['customer_type'],
                'phoneNumber': row['phone_number'],
                'wifiInfo': row['wifi_info'],
                'totalAmount': row['total_amount'],
                'discount': row['discount'],
                'paymentMethod': row['payment_method'],
                'otherInfo': row['other_info'],
                'itemsPurchased': json.loads(row['items_purchased']) if row['items_purchased'] else []
            }
        })
    else:
        return jsonify({'error': 'Invoice info not found for image_index {}'.format(image_index)}), 404


########################POST#########################################################

# Function to call the NLP model via the API and return structured JSON data
async def call_nlp_model_async(prompt: str) -> dict:
    async with ClientSession() as session:
        data = {
           # "model":"claude-3-5-sonnet-20240620",
           # "model": "gemini-1.5-flash-002",
            # "model":"gemini-1.5-flash-latest",
            "model": "gpt-3.5-turbo",
            #"model":"gpt-3.5-turbo-1106",
            # "model":"gpt-4-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000,
            "temperature": 0.2
        }
        async with session.post(url, headers=headers, json=data) as response:
            # Sử dụng response.status thay vì response.status_code
            if response.status == 200:
                try:
                    reply_content = await response.json()  # Sử dụng await vì response.json() là async
                    reply_content = reply_content['choices'][0]['message']['content']
                    json_start = reply_content.find('{')
                    json_end = reply_content.rfind('}') + 1
                    json_str = reply_content[json_start:json_end]
                    result = json.loads(json_str)
                    return result  # Trả về kết quả xử lý thành công
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print("Model response:", reply_content)
                    return {}  # Trả về rỗng nếu lỗi giải mã JSON
                except Exception as e:
                    print(f"Error in processing NLP response: {e}")
                    return {}  # Trả về rỗng nếu có lỗi khác
            else:
                print(f"Error: {response.status}, {await response.text()}")  # Sử dụng response.status thay vì status_code
                return {}  # Trả về rỗng nếu mã trạng thái không phải 200

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# API để trả về hình ảnh từ thư mục local
@app.route('/api/uploads/<filename>', methods=['GET'])
async def uploaded_file(filename):
    # Kiểm tra và xác nhận file có tồn tại trong thư mục
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return "File not found", 404
# API POST hình ảnh và xử lý OCR cùng mô hình NLP
ocr = PaddleOCR(
        lang="latin",  # Sử dụng cả tiếng Anh và tiếng Việt
        use_angle_cls=True,
        det_model_dir="Multilingual_PP-OCRv3_det_infer",
        rec_model_dir="latin_PP-OCRv3_rec_infer",
        cls_model_dir="ch_ppocr_mobile_v2.0_cls_slim_infer",
        # det_model_dir="ch_PP-OCRv3_det_infer",
        # rec_model_dir="ch_PP-OCRv3_rec_infer",
        # cls_model_dir="ch_ppocr_mobile_v2.0_cls_infer",
        show_log=True,
        # det_db_thresh=0.5,
        # det_db_unclip_ratio=1.7,
        # drop_score=0.01,
        max_batch_size=4,
        gpu_mem=3050,
        total_process_num=8,
        use_cuda=True,
        use_gpu=True,
        ocr_version='PP-OCRv4',
        use_space_char=True
    )
@app.route('/api/upload_image', methods=['POST'])
async def upload_image():
    if 'image' not in request.files or request.files['image'].filename == '':
        return jsonify({"error": "No image file provided"}), 400

        # Nhận file ảnh
    image = request.files['image']

    # Kiểm tra định dạng file
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if not allowed_file(image.filename):
        return jsonify({"error": "Unsupported file type. Only PNG, JPG, JPEG, BMP, and TIFF are allowed"}), 400

    # Đọc dữ liệu ảnh từ buffer
    npimg = np.frombuffer(image.read(), np.uint8)
    if npimg.size == 0:
        return jsonify({"error": "Uploaded file is empty or invalid"}), 400

    # Giải mã ảnh với OpenCV
    img = cv.imdecode(npimg, cv.IMREAD_COLOR)
    if img is None:
        return jsonify({"error": "Failed to decode the image. Invalid file format"}), 400

    # Lưu ảnh vào thư mục 'uploads' và tạo đường dẫn cục bộ
    upload_folder = "uploads"  # Thư mục lưu ảnh
    os.makedirs(upload_folder, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
    timestamp = int(time.time())  # Lấy thời gian hiện tại tính theo giây
    image_filename = f"{timestamp}_{secure_filename(image.filename)}"
    image_path = os.path.join(upload_folder, image_filename)
    # Save the image using imwrite
    cv.imwrite(image_path, img)

    # Đường dẫn cục bộ (trên máy tính)
    # image_url = os.path.abspath(image_path)  # Đường dẫn tuyệt đối
    image_url = image_filename

    # Preprocess hình ảnh
    _, preprocessed_img = preprocess(img)
    height,width = img.shape[:2]
    if height < 1000 and width < 1000:
        img = cv.resize(img, (width * 2, height * 2))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    # img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    ocr_result = ocr.ocr(preprocessed_img)
    ocr_ogri = ocr.ocr(img)


    if not ocr_result or len(ocr_result) == 0:
        return jsonify({"error": "No text found in the image."}), 400
    print(len(ocr_ogri[0]))
    print(len(ocr_result[0]))
    a= len(ocr_ogri[0])
    b= len(ocr_result[0])


    bboxes, text_confs = zip_longest(*ocr_result[0], fillvalue=None)
    texts_confs = [tc if tc is not None else ("", 0.0) for tc in text_confs]
    texts, confs = zip(*texts_confs)
    extracted_text = " ".join([text for text in texts if text])
    print(len(extracted_text))
    ocr_img = draw_ocr(
        preprocessed_img, bboxes, txts=None, scores=confs, drop_score=0.5)
    ocr_img = cv.cvtColor(ocr_img, cv.COLOR_GRAY2BGR)

    bboxes1, text_confs1 = zip_longest(*ocr_ogri[0], fillvalue=None)
    texts_confs1 = [tc if tc is not None else ("", 0.0) for tc in text_confs1]
    texts1, confs1 = zip(*texts_confs1)
    extracted_text1 = " ".join([text for text in texts1 if text])
    print(len(extracted_text1))
    ocrimg = f"{image_filename}_ocr.jpg"
    ocr_image_path = os.path.join(upload_folder, f"{image_filename}_ocr.jpg")
    cv.imwrite(ocr_image_path, ocr_img)

    if(len(extracted_text1) >len(extracted_text)):
        extracted_text = extracted_text1
        ocr_img = draw_ocr(
            img, bboxes1, txts=None, scores=confs1, drop_score=0.5)
        ocr_img = cv.cvtColor(ocr_img, cv.COLOR_BGR2RGB)
    # Save OCR image with bounding boxes and confidence scores
    # Lưu ảnh đã detect vào thư mục
        ocrimg = f"{image_filename}_ocr.jpg"
        ocr_image_path = os.path.join(upload_folder, f"{image_filename}_ocr.jpg")
        cv.imwrite(ocr_image_path, ocr_img)

    # Lấy đường dẫn tuyệt đối của ảnh đã lưu
    # detected_image_url = os.path.abspath(ocr_image_path)
    detected_image_url = ocrimg
    # Tạo prompt cho API NLP để xử lý văn bản và lấy thông tin hóa đơn
    prompt = f"""
    Please correct any spelling mistakes in the following text extracted from an image, and then extract the necessary invoice information,
    Add accents if the text is in Vietnamese.
    Extract the following details: 
    - **image_url**
    - **detected_image_url**
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
        "image_index":"",
        "detected_image_url":"",
        "image_url": "",
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

    # Gọi NLP API để xử lý văn bản và lấy thông tin hóa đơn
    nlp_result =  await call_nlp_model_async(prompt)
    corrected_text = nlp_result.get("correctedText", "")
    invoice_info = nlp_result.get("invoiceInfo", {})

    # Chuyển đổi các giá trị cần thiết sang định dạng phù hợp
    total_amount = invoice_info.get('totalAmount', '0')
    discount = str(invoice_info.get('discount', '0'))

    # Nếu other_info trống, sử dụng corrected_text
    other_info = invoice_info.get('otherInfo', [])
    if not other_info:
        other_info.append(corrected_text)

    # Kiểm tra nếu any item in other_info là dict, chuyển đổi chúng thành chuỗi
    other_info_str = ' '.join([str(item) if not isinstance(item, str) else item for item in other_info])

    # Lưu thông tin hóa đơn vào MySQL
    conn = await  get_db_connection()
    async with conn.cursor() as cursor:
        query = """
            INSERT INTO invoices (
                image_url,detected_image_url,texts, corrected_text, company_name, address, date_of_sale, 
                invoice_number, cashier, table_info, customer_type, phone_number, wifi_info, 
                email, tax_id, invoice_type, total_amount, discount, payment_method, 
                other_info, items_purchased
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            image_url,
            detected_image_url,
            extracted_text,
            corrected_text,
            invoice_info.get('CompanyName', ''),
            invoice_info.get('address', ''),
            invoice_info.get('dateOfSale', ''),
            invoice_info.get('invoiceNumber', ''),
            invoice_info.get('cashier', ''),
            invoice_info.get('table', ''),
            invoice_info.get('customerType', ''),
            invoice_info.get('phoneNumber', ''),
            invoice_info.get('wifiInfo', ''),
            invoice_info.get('email', ''),
            invoice_info.get('taxId', ''),
            invoice_info.get('invoiceType', ''),
            total_amount,
            discount,
            invoice_info.get('paymentMethod', ''),
            other_info_str,
            json.dumps(invoice_info.get('itemsPurchased', []))  # Lưu danh sách các sản phẩm được mua dưới dạng JSON
        )

        await cursor.execute(query, values)
        await conn.commit()

    cursor.close()
    conn.close()
    # Chuyển items_purchased thành chuỗi JSON
    items_purchased_str = json.dumps(invoice_info.get('itemsPurchased', []), ensure_ascii=False, indent=10)

    # Chuyển items_purchased_str từ chuỗi JSON thành list
    items_purchased = json.loads(items_purchased_str)

    # Tạo DataFrame từ list hoặc dictionary
    if isinstance(items_purchased, list):
        df_items_purchased = pd.DataFrame(items_purchased)
    else:
        df_items_purchased = pd.DataFrame(
            [items_purchased])  # Nếu là dictionary thì chuyển thành DataFrame với một dòng duy nhất
    # Tạo một dictionary mới chứa các trường có giá trị
    response_data = {
        "image_url": image_url,
        "detected_image_url": detected_image_url,
        "corrected_text": corrected_text,
        "message": "Invoice data added to database"
    }

    # Chỉ thêm các trường có giá trị (không trống) vào response_data
    fields = [
        ("company_name", invoice_info.get('CompanyName', '')),
        ("address", invoice_info.get('address', '')),
        ("date_of_sale", invoice_info.get('dateOfSale', '')),
        ("invoice_number", invoice_info.get('invoiceNumber', '')),
        ("cashier", invoice_info.get('cashier', '')),
        ("table_info", invoice_info.get('table', '')),
        ("customer_type", invoice_info.get('customerType', '')),
        ("phone_number", invoice_info.get('phoneNumber', '')),
        ("wifi_info", invoice_info.get('wifiInfo', '')),
        ("email", invoice_info.get('email', '')),
        ("tax_id", invoice_info.get('taxId', '')),
        ("invoice_type", invoice_info.get('invoiceType', '')),
        ("total_amount", invoice_info.get('totalAmount', '')),
        ("discount", invoice_info.get('discount', '')),
        ("payment_method", invoice_info.get('paymentMethod', '')),
    ]

    # Lọc các trường có giá trị không trống
    for field, value in fields:
        if value:
            response_data[field] = value

        # Nếu có items_purchased, thêm vào response_data dưới dạng DataFrame
    if not df_items_purchased.empty:
        response_data["items_purchased"] = df_items_purchased.to_dict(
            orient='records')  # Chuyển DataFrame thành list of dicts
    print(df_items_purchased)
    # Kiểm tra 'other_info' và chỉ trả về nếu có giá trị
    if invoice_info.get('otherInfo', []):
        response_data["other_info"] = other_info_str

    # Trả về phản hồi JSON
    return jsonify(response_data), 200

####################################PUT#######################################################
@app.route('/api/update_invoice/<int:image_index>', methods=['PUT'])
def update_invoice(image_index):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Đặt chế độ dictionary=True để trả về kết quả dưới dạng dictionary
    # Lấy dữ liệu từ request body
    data = request.get_json()

    query = """
        UPDATE invoices
        SET company_name = %s,
            address = %s,
            date_of_sale = %s,
            invoice_number = %s,
            cashier = %s,
            table_info = %s,
            customer_type = %s,
            phone_number = %s,
            wifi_info = %s,
            email = %s,
            tax_id = %s,
            invoice_type = %s,
            total_amount = %s,
            discount = %s,
            payment_method = %s,
            other_info = %s,
            items_purchased = %s
        WHERE image_index = %s
    """

    # Chuỗi hóa các thông tin khác nếu cần
    other_info = ', '.join(data.get('otherInfo', []))
    items_purchased = json.dumps(data.get('itemsPurchased', []))

    values = (
        data.get('companyName', ''),
        data.get('address', ''),
        data.get('dateOfSale', ''),
        data.get('invoiceNumber', ''),
        data.get('cashier', ''),
        data.get('table', ''),
        data.get('customerType', ''),
        data.get('phoneNumber', ''),
        data.get('wifiInfo', ''),
        data.get('email', ''),
        data.get('taxId', ''),
        data.get('invoiceType', ''),
        data.get('totalAmount', '0'),
        data.get('discount', '0'),
        data.get('paymentMethod', ''),
        other_info,
        items_purchased,
        image_index
    )

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount > 0:
        # Nếu cập nhật thành công, lấy lại thông tin đã cập nhật
        cursor.execute("SELECT * FROM invoices WHERE image_index = %s", (image_index,))
        updated_invoice = cursor.fetchone()
        message = f"Invoice with image_index {image_index} has been updated."
        status = 200
    else:
        updated_invoice = None
        message = f"Invoice with image_index {image_index} not found."
        status = 404

    cursor.close()
    conn.close()

    # Trả về thông tin hóa đơn đã được cập nhật
    return jsonify({"message": message, "updated_invoice": updated_invoice}), status



####################################DELETE#######################################################   

@app.route('/api/delete_invoice/<int:image_index>', methods=['DELETE'])
async def delete_invoice(image_index):
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        query = "DELETE FROM invoices WHERE image_index = %s"
        await cursor.execute(query, (image_index,))
        await conn.commit()

        if cursor.rowcount > 0:
            message = f"Invoice with image_index {image_index} has been deleted."
            status = 200
        else:
            message = f"Invoice with image_index {image_index} not found."
            status = 404
    cursor.close()
    conn.close()
    return jsonify({"message": message}), status
###################################Main#########################################################

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(app.run(debug=False, threaded=True))
     app.run(debug=False, threaded=True)
