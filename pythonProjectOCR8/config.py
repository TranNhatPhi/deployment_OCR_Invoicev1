# config.py

api_key = ""  # key
url = ""  # url key

# Bạn có thể tạo một template cho prompt nếu cần sử dụng nhiều nơi
default_prompt_template = """
Please extract the necessary commercial invoice information from the following text:
Extract the following details in the correct format:
- **Invoice Information**:
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
  - Total Amount (sum of all items)
  - Gross Weight
  - Net Weight

Provide the output in the following JSON format:

{
    "shipperInfo": {
        "companyName": "",
        "address": "",
        "phoneNumber": ""
    },
    "consigneeInfo": {
        "companyName": "",
        "address": "",
        "phoneNumber": ""
    },
    "invoiceNumber": "",
    "invoiceDate": "",
    "portOfLoading": "",
    "portOfDischarge": "",
    "termsOfPayment": "",
    "shippingMethod": "",
    "itemsPurchased": [
        {
            "name": "",
            "quantity": "",
            "unitPrice": "",
            "totalPrice": ""
        }
    ],
    "totalAmount": "",
    "grossWeight": "",
    "netWeight": ""
}
"""
