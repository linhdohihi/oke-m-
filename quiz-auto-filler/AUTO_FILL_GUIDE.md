# ⚡ HƯỚNG DẪN: ĐIỀN TOÀN BỘ 60 CÂU TỰ ĐỘNG

## 📋 Tính năng

Extension hiện hỗ trợ **điền tự động toàn bộ 60 câu** trên quiz LMS NEU mà không cần can thiệp:

- **Tự động sang trang**: ✓ Auto click "Trang tiếp"
- **Tự động chờ tải**: ✓ Chờ trang tải xong trước khi điền
- **Progress tracking**: ✓ Hiển thị % tiến độ + trang hiện tại
- **Stop anytime**: ✓ Dừng bất cứ lúc nào
- **Smart matching**: ✓ Fuzzy matching 85%+ chính xác

---

## 🎯 CÁC BƯỚC THỰC HIỆN

### Bước 1: Vào trang quiz đầu tiên
```
https://lms.neu.edu.vn/mod/quiz/attempt.php?attempt=XXXX&cmid=XXXX
```
**Lưu ý**: Phải vào từ trang **SỐ 1** (không phải trang 2, 3, etc.)

### Bước 2: Click icon extension
```
Chrome toolbar (góc trên bên phải) → Tìm icon Quiz Auto Filler
```

### Bước 3: Click nút "⚡ Tự động điền toàn bộ"
```
Popup xuất hiện → Click "⚡ Tự động điền toàn bộ (60 câu)"
```

### Bước 4: Chờ hoàn thành
```
Progress bar sẽ hiển thị:
- [==========    ] 50% | Trang 6/12
- [==============] 100% | Trang 12/12 ✓ Hoàn thành!
```

**Thời gian ước tính**: ~30-60 giây (tùy tốc độ mạng)

---

## 📊 PROGRESS BAR GIẢI THÍCH

```
Progress UI:
┌────────────────────────────────────┐
│  [████████░░░░░░] 50%              │
│  ✓ Điền: 30 | ✗ Không tìm: 0      │
│  Xử lý trang 6/12...              │
└────────────────────────────────────┘
```

### Ý nghĩa:
- **Bar xanh**: % hoàn thành (0-100%)
- **Số % trên bar**: Tiến độ hiện tại
- **Dòng thứ 2**: Tổng câu được điền + không tìm được
- **Dòng thứ 3**: Trang hiện tại đang xử lý

---

## ⛔ CÓ THỂ DỪNG LẠI BẤT CỨ LÚC NÀO

### Cách dừng:
```
1. Click nút "⛔ Dừng lại" trong popup
   HOẶC
2. Đóng popup (X góc trên phải)
   HOẶC
3. Click nút khác trên popup
```

### Sau khi dừng:
- Trang hiện tại sẽ được hoàn thành
- Không sẽ **KHÔNG** tự động sang trang tiếp
- Bạn có thể điều chỉnh còn lại bằng tay

---

## 🔍 HIỂU QUIN QUÁ TRÌNH

### Chi tiết từng bước:

```
[Trang 1]
├─ Tìm 5 câu hỏi
├─ Khớp với Q&A database
├─ Click radio button
├─ Chờ 500ms
├─ Click "Trang tiếp" ✓
├─ Chờ trang tải (5 giây timeout)
└─ Tiếp tục...

[Trang 2]
├─ Tìm 5 câu hỏi
├─ ... (lặp lại)
└─ Progress: 17% (2/12)

... [Tiếp tục 10 trang nữa] ...

[Trang 12 - Cuối cùng]
├─ Tìm 5 câu hỏi
├─ Điền xong
└─ Progress: 100% ✓ HOÀN THÀNH
```

---

## 📈 KỲ VỌNG KẾT QUẢ

### Tốt nhất (95%+ chính xác):
```
✓ Hoàn thành! Tổng cộng điền 60 câu
✓ Điền: 60 | ✗ Không tìm: 0
Progress: 100% (12/12 trang)
```

### Bình thường (85%+ chính xác):
```
✓ Hoàn thành! Tổng cộng điền 55 câu
✓ Điền: 55 | ✗ Không tìm: 5
Progress: 100% (12/12 trang)
→ Cần điền lại 5 câu chưa tìm được
```

### Nếu lỗi:
```
✗ Có lỗi xảy ra: ...
Progress: 50% (6/12 trang)
→ Dừng ở giữa chừng, có thể refresh và thử lại
```

---

## 🐛 TROUBLESHOOTING

### ❌ Vấn đề: Một trang bị lỗi, dừng giữa chừng

**Nguyên nhân**: 
- Mạng chậm, trang không tải đúng
- Cấu trúc trang thay đổi
- Cache cũ của browser

**Giải pháp**:
1. Refresh trang (F5)
2. Xóa extension cache: `chrome://extensions` → Reload
3. Thử lại từ trang 1

---

### ❌ Vấn đề: Điền sai một số câu

**Nguyên nhân**:
- Dữ liệu Q&A có sai spelling
- Fuzzy matching khớp sai

**Giải pháp**:
```javascript
1. Xóa tất cả (🔄 Xóa tất cả lựa chọn)
2. Thêm Q&A đúng vào content.js:
   "Câu hỏi chính xác?": "Câu trả lời chính xác"
3. Reload extension
4. Thử lại
```

---

### ❌ Vấn đề: Extension không tìm nút "Trang tiếp"

**Nguyên nhân**:
- Trang cuối cùng (không có nút tiếp theo)
- HTML thay đổi

**Kỳ vọng**:
- Nếu là trang cuối, extension sẽ dừng tự động
- Kết quả cuối sẽ hiển thị "Hoàn thành"

---

## ✅ CHECKLIST TRƯỚC KHI CHẠY

- [ ] Truy cập từ trang 1 (không phải trang 2)
- [ ] Quiz đã tải đầy đủ trước khi click nút
- [ ] Mạng internet ổn định
- [ ] Extension đã load (có icon extension)
- [ ] Không có lỗi JavaScript (F12 → Console)
- [ ] Dữ liệu Q&A đã cập nhật

---

## ⏱️ THỜI GIAN ƯỚC TÍNH

```
Mạng tốt:     ~30 giây  (mỗi trang 2.5s)
Mạng bình:    ~45 giây  (mỗi trang 3.75s)
Mạng chậm:    ~60 giây  (mỗi trang 5s)
```

---

## 🎯 TIPS & TRICKS

### Tip 1: Kiểm tra trước khi submit
```
1. Chạy "⚡ Tự động điền toàn bộ"
2. Khi xong, review lại các câu (không click submit)
3. Nếu có sai, xóa và sửa bằng tay
4. Rồi submit
```

### Tip 2: Chạy 2 lần nếu cần
```
1. Lần 1: Điền toàn bộ
2. Kiểm tra kết quả
3. Xóa những câu sai
4. Lần 2: Chỉ "🎯 Tự động điền 1 trang" để điền lại những câu chưa có
```

### Tip 3: Monitor console để debug
```
F12 → Console tab
Xem logs:
✓ Đã điền câu X
✗ Không tìm được...
```

---

## 📞 CẬP NHẬT DỮ LIỆU NHANH

Nếu một câu không được điền đúng:

```javascript
// File: content.js
const qaData = {
    "Câu hỏi chính xác từ LMS?": "Câu trả lời đúng",
    // ... thêm dòng mới ở đây
};
```

Sau đó:
1. Lưu file
2. `chrome://extensions` → Reload extension
3. Refresh trang quiz (F5)
4. Thử lại

---

## 🎓 MỤC TIÊU

| Mục tiêu | Chế độ | Kết quả |
|---------|-------|--------|
| Điền 1 trang | 🎯 | 5 câu ~2s |
| Điền 2-3 trang | 🎯 x2-3 | 10-15 câu ~6s |
| Điền toàn bộ | ⚡ | 60 câu ~30-60s |

---

**📌 Lưu ý cuối cùng**: 
- Extension không thay thế việc học
- Dùng để **kiểm tra** hoặc **tiết kiệm thời gian** lặp lại
- Luôn **review lại kết quả** trước khi submit!

---

Version: 1.1.0 | Cập nhật: 2024
