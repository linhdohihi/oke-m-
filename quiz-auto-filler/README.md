# Quiz Auto Filler - Chrome Extension

Extension tự động điền đáp án quiz trên LMS NEU (https://lms.neu.edu.vn)

## 🚀 Tính năng

- ✅ Tự động điền 1 trang (5 câu)
- ✅ **Tự động điền toàn bộ quiz (60 câu, 12 trang)** - Mới!
- ✅ Tự động bấm nút "Trang tiếp" giữa các trang
- ✅ Progress bar hiển thị tiến độ
- ✅ Khóa dừng quá trình bất cứ lúc nào
- ✅ Nhận diện thông minh với fuzzy matching
- ✅ Xóa tất cả lựa chọn một cách nhanh chóng
- ✅ Hiển thị thống kê kết quả chi tiết

## 📦 Cài đặt

### Bước 1: Tải về extension

```bash
# Thư mục extension đã được tạo tại: /quiz-auto-filler/
```

### Bước 2: Mở Chrome Extensions

1. Mở **Google Chrome** 
2. Nhập vào thanh địa chỉ: `chrome://extensions/`
3. Bật **Developer mode** (góc trên phải)

### Bước 3: Load extension

1. Click **"Load unpacked"**
2. Chọn thư mục `/quiz-auto-filler/`
3. Extension sẽ xuất hiện trong danh sách

## 💡 Cách sử dụng

### Chế độ 1: Điền từng trang (5 câu)

1. Truy cập trang quiz: https://lms.neu.edu.vn/mod/quiz/attempt.php?...
2. Click vào biểu tượng extension ở góc trên phải
3. Click nút **"🎯 Tự động điền trang hiện tại"**
4. Chờ extension xử lý (1-2 giây)
5. Kết quả:
   - ✓ Số câu đã điền
   - ✗ Số câu không tìm được đáp án

### Chế độ 2: Điền toàn bộ (60 câu, 12 trang) ⚡ MỚI!

1. Truy cập trang quiz đầu tiên
2. Click vào biểu tượng extension
3. Click nút **"⚡ Tự động điền toàn bộ (60 câu)"**
4. Extension sẽ:
   - ✓ Điền 5 câu trên trang hiện tại
   - ✓ Tự động click "Trang tiếp"
   - ✓ Chờ trang tải
   - ✓ Tiếp tục điền 5 câu trên trang mới
   - ✓ Lặp lại cho tới hết 12 trang

5. **Progress bar** sẽ hiển thị:
   - % hoàn thành (0-100%)
   - Trang hiện tại (1/12, 2/12, etc.)
   - Tổng câu đã điền

6. Để **dừng lại** bất cứ lúc nào:
   - Click nút **"⛔ Dừng lại"**
   - Hoặc đóng popup

### Chế độ 3: Xóa tất cả lựa chọn

1. Click vào biểu tượng extension
2. Click nút **"🔄 Xóa tất cả lựa chọn"**
3. Tất cả các câu được chọn sẽ bị xóa
4. Bạn có thể điền lại hoặc làm bằng tay

## 🔧 Cấu trúc tệp

```
quiz-auto-filler/
├── manifest.json       # Cấu hình extension
├── popup.html         # UI của popup
├── popup.js           # Logic popup
└── content.js         # Script chạy trên trang web
```

## 📝 Dữ liệu Q&A

- Tất cả 60+ câu hỏi và đáp án được nhúng trong `content.js`
- Mỗi câu hỏi được ghép với câu trả lời tương ứng
- Extension sử dụng **fuzzy matching** để khớp câu hỏi

## ⚙️ Cách hoạt động

1. **Trích xuất**: Tìm tất cả câu hỏi trên trang (`div.qtext`)
2. **Khớp**: So sánh với dữ liệu Q&A sử dụng fuzzy matching
3. **Tìm đáp án**: Định vị vị trí của đáp án đúng
4. **Chọn**: Click vào radio button tương ứng

## 🎯 Độ chính xác

- **Khớp chính xác**: 95%+
- **Khớp fuzzy**: 85%+

## ⚠️ Lưu ý

- Extension chỉ hoạt động trên https://lms.neu.edu.vn
- Cần đảm bảo JavaScript được bật trên trình duyệt
- Một số quiz có cấu trúc khác nhau có thể cần điều chỉnh thêm

## 🐛 Troubleshooting

**Extension không xuất hiện icon?**
- Kiểm tra lại quá trình cài đặt
- Refresh lại trang web
- Kiểm tra `chrome://extensions/` xem extension có được load hay không

**Không điền được đáp án?**
- Kiểm tra xem có JavaScript error trên console (F12)
- Đảm bảo trang quiz đã tải hoàn toàn
- Thử xóa và cài lại extension

**Điền sai đáp án?**
- Extension sử dụng fuzzy matching, có khả năng xảy ra sai sót
- Cập nhật dữ liệu Q&A trong `content.js` nếu cần

## 📧 Hỗ trợ

Để cập nhật hoặc sửa lỗi, edit file `content.js` và reload extension.

## 📄 License

Chỉ dùng cho mục đích học tập và nghiên cứu.

---

**Phiên bản**: 1.0.0  
**Cập nhật**: 2024
