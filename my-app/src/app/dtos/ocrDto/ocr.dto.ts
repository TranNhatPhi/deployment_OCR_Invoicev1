import { IsNumber } from 'class-validator';
import firebase from "firebase/compat";
import Item = firebase.analytics.Item;

export class ocrDto  {
  texts: string;                    // Văn bản gốc trích xuất từ hóa đơn
  corrected_text: string;           // Văn bản đã được sửa lỗi (nếu có)
  company_name: string;             // Tên công ty
  buyer_name: string;               // Tên người mua
  buyer_address: string;            // Địa chỉ người mua
  address: string;                  // Địa chỉ giao hàng
  date_of_sale: string;             // Ngày bán
  invoice_number: string;           // Số hóa đơn
  cashier: string;                  // Tên thu ngân
  table_info: string;               // Thông tin bàn (nếu có)
  customer_type: string;            // Loại khách hàng
  phone_number: string;             // Số điện thoại
  wifi_info: string;                // Thông tin wifi (nếu có)
  email: string;                    // Email khách hàng
  tax_id: string;                   // Mã số thuế
  invoice_type: string;             // Loại hóa đơn (ví dụ: hóa đơn GTGT, hóa đơn bán lẻ)
  total_amount: string;             // Tổng số tiền (trước/bao gồm thuế)
  discount: string;                 // Mức giảm giá (nếu có)
  tax_rate: string;                 // Tỷ lệ thuế
  tax_amount: string;               // Số tiền thuế
  payment_method: string;           // Phương thức thanh toán (tiền mặt, thẻ, v.v.)
  shipping_method: string;          // Phương thức vận chuyển (nếu có)
  shipping_cost: string;            // Chi phí vận chuyển (nếu có)
  other_info: string;               // Thông tin khác (nếu có)
  items_purchased: string         // Danh sách các mục đã mua
  created_at: string;               // Thời gian tạo hóa đơn
  updated_at: string;               // Thời gian cập nhật hóa đơn
  image_url: string;                // URL của ảnh hóa đơn đã tải lên
  detected_image_url: string;       // URL của ảnh hóa đơn sau khi phát hiện thông tin

  constructor(data: any) {
    this.texts = data.texts;
    this.corrected_text = data.corrected_text;
    this.company_name = data.company_name;
    this.buyer_name = data.buyer_name;
    this.buyer_address = data.buyer_address;
    this.address = data.address;
    this.date_of_sale = data.date_of_sale;
    this.invoice_number = data.invoice_number;
    this.cashier = data.cashier;
    this.table_info = data.table_info;
    this.customer_type = data.customer_type;
    this.phone_number = data.phone_number;
    this.wifi_info = data.wifi_info;
    this.email = data.email;
    this.tax_id = data.tax_id;
    this.invoice_type = data.invoice_type;
    this.total_amount = data.total_amount;
    this.discount = data.discount;
    this.tax_rate = data.tax_rate;
    this.tax_amount = data.tax_amount;
    this.payment_method = data.payment_method;
    this.shipping_method = data.shipping_method;
    this.shipping_cost = data.shipping_cost;
    this.other_info = data.other_info;
    this.items_purchased = data.items_purchased;
    this.created_at = data.created_at;
    this.updated_at = data.updated_at;
    this.image_url = data.image_url;
    this.detected_image_url = data.detected_image_url;
  }
}
