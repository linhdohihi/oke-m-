# 🎓 HƯỚNG DẪN CÀI ĐẶT CHI TIẾT

## 📋 Yêu cầu
- Google Chrome (Latest version)
- Trình duyệt hỗ trợ Chrome Extensions
- File thư mục `quiz-auto-filler`

---

## ⚡ CÀI ĐẶT NHANH (5 phút)

### Bước 1️⃣: Mở Chrome Extensions Manager
```
1. Mở Google Chrome
2. Gõ địa chỉ: chrome://extensions/
3. Hoặc: Menu (⋮) → Thêm công cụ → Tiện ích mở rộng
```

### Bước 2️⃣: Kích hoạt Developer Mode
```
Góc trên phải trang Extensions Manager
   ↓
Toggle "Developer mode" → ENABLED ✓
```

### Bước 3️⃣: Load Extension
```
Click nút "Load unpacked"
   ↓
Chọn thư mục "quiz-auto-filler"
   ↓
Extension sẽ xuất hiện trong danh sách ✓
```

### Bước 4️⃣: Kiểm tra cài đặt
```
✓ Icon extension xuất hiện ở góc trên phải
✓ Status: "Enabled"
✓ Truy cập tab "Details" để xem version
```

---

## 📱 SỬ DỤNG

### Lần đầu sử dụng
```
1. Truy cập: https://lms.neu.edu.vn/mod/quiz/attempt.php?...
2. Trang quiz tải xong
3. Click 🧩 icon extension ở góc trên phải
4. Popup xuất hiện với 2 nút:
   - 🎯 Tự động điền đáp án
   - 🔄 Xóa tất cả lựa chọn
5. Click "Tự động điền đáp án"
6. Chờ xử lý (1-3 giây)
7. Kết quả hiển thị:
   ✓ Điền: X câu
   ✗ Không tìm: Y câu
```

### Quy trình hoàn chỉnh
```
[1] Mở quiz trên LMS
       ↓
[2] Bấm nút extension
       ↓
[3] Chọn "Tự động điền đáp án"
       ↓
[4] Xem kết quả
       ↓
[5] Nếu cần xóa → Click "Xóa tất cả lựa chọn"
       ↓
[6] Submit quiz hoặc điều chỉnh nếu cần
```

---

## 🔧 CONFIGURE DỮ LIỆU

### Thêm câu hỏi mới

1. Mở file: `quiz-auto-filler/content.js`
2. Tìm object `qaData = { ... }`
3. Thêm dòng mới:
```javascript
"Câu hỏi của bạn?": "Câu trả lời của bạn.",
```

4. Lưu file
5. Reload extension: `chrome://extensions` → Click refresh icon

### Ví dụ:
```javascript
const qaData = {
    "Câu hỏi 1?": "Câu trả lời 1",
    "Câu hỏi 2?": "Câu trả lời 2",
    "Câu hỏi mới?": "Câu trả lời mới",  // ← Thêm dòng này
};
```

---

## 🐛 CÁC VẤN ĐỀ THƯỜNG GẶP

### ❌ Vấn đề 1: Extension không xuất hiện
**Nguyên nhân**: Extension không được load đúng
**Giải pháp**:
- Kiểm tra developer mode: ON
- Kiểm tra đường dẫn thư mục: Đúng?
- Kiểm tra manifest.json: Tồn tại? Hợp lệ?

### ❌ Vấn đề 2: Không thể click nút "Tự động điền"
**Nguyên nhân**: Content script chưa load trên trang
**Giải pháp**:
- Refresh lại trang quiz (F5)
- Đảm bảo URL: `https://lms.neu.edu.vn/mod/quiz/...`
- Kiểm tra Console: F12 → Console tab

### ❌ Vấn đề 3: Điền đáp án sai
**Nguyên nhân**: Fuzzy matching không đủ chính xác
**Giải pháp**:
- Cập nhật Q&A data
- Kiểm tra spelling của câu hỏi
- Report bug và provide ví dụ

### ❌ Vấn đề 4: Không điền được một số câu
**Nguyên nhân**: Câu hỏi không có trong dữ liệu
**Giải pháp**:
- Thêm câu hỏi vào `qaData`
- Sử dụng "Xóa tất cả" và điền lại
- Kiểm tra xem câu trả lời có khớp không

---

## 📊 KIỂM TRA DEBUG

### Mở Developer Tools
```
F12 hoặc Right-click → Inspect
```

### Xem logs
```
Console tab → Tìm message "Quiz Auto Filler extension loaded!"
```

### Xem errors
```
Tiền tố: ✗ = Lỗi
Tiền tố: ✓ = Thành công
```

---

## 🎯 TIPS & TRICKS

### Tip 1: Xóa nhanh để làm lại
```
Bấm icon extension → "🔄 Xóa tất cả lựa chọn"
Sau đó "🎯 Tự động điền đáp án" lại
```

### Tip 2: Kiểm tra chi tiết
```
F12 → Console tab
Tìm message: "✓ Đã điền câu X:"
Hoặc: "✗ Không tìm được câu hỏi:"
```

### Tip 3: Cập nhật extension
```
Sửa file content.js
Chrome://extensions → Click refresh icon
Reload trang quiz (F5)
```

---

## 📁 STRUCTURE CỦA FILES

```
quiz-auto-filler/
│
├── 📄 manifest.json
│   └── Cấu hình extension (permissions, scripts, etc.)
│
├── 📄 popup.html
│   └── Giao diện popup (buttons, status, stats)
│
├── 📜 popup.js
│   └── Xử lý sự kiện nút bấm từ popup
│
├── 📜 content.js
│   ├── Dữ liệu Q&A (60+ Q&A pairs)
│   ├── Hàm trích xuất câu hỏi từ trang
│   ├── Hàm khớp câu hỏi (fuzzy matching)
│   ├── Hàm điền đáp án
│   └── Hàm xóa lựa chọn
│
└── 📖 README.md
    └── Hướng dẫn cơ bản
```

---

## ✅ CHECKLIST CÀI ĐẶT

- [ ] Tải thư mục `quiz-auto-filler`
- [ ] Mở `chrome://extensions/`
- [ ] Bật "Developer mode"
- [ ] Click "Load unpacked"
- [ ] Chọn thư mục `quiz-auto-filler`
- [ ] Kiểm tra icon extension xuất hiện
- [ ] Truy cập quiz trên LMS
- [ ] Test bấm nút "Tự động điền đáp án"
- [ ] Xác nhận các câu được điền
- [ ] Test bấm nút "Xóa tất cả lựa chọn"

---

## 🆘 CẦN GIÚP ĐỠ?

### Kiểm tra logs
```
F12 → Console → Xem message
```

### Thử reset
```
1. Remote extension từ chrome://extensions/
2. Reload lại từ thư mục `quiz-auto-filler`
3. Restart Chrome nếu cần
```

### Cập nhật dữ liệu
```
1. Edit content.js
2. Thêm/sửa Q&A pairs
3. Save file
4. Reload extension
5. Test lại
```

---

## 📞 CONTACT & SUPPORT

Nếu có vấn đề:
1. Kiểm tra lại các bước cài đặt
2. Xem logs trong Console (F12)
3. Cập nhật dữ liệu Q&A nếu cần
4. Report bug với ví dụ cụ thể

---

**🎉 Chúc bạn sử dụng extension thành công!**

Version: 1.0.0 | Last Updated: 2024
