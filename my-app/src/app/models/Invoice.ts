

export interface Invoice {
  image_index: number;              // ID của ảnh hóa đơn (auto increment)
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
  items_purchased: object;          // Danh sách các mục đã mua
  created_at: string;               // Thời gian tạo hóa đơn
  updated_at: string;               // Thời gian cập nhật hóa đơn
  image_url: string;                // URL của ảnh hóa đơn đã tải lên
  detected_image_url: string;       // URL của ảnh hóa đơn sau khi phát hiện thông tin
}
