# PDF Question Extractor Tool 🎯

A comprehensive tool để trích xuất câu hỏi, đáp án và đáp án chính xác từ các file PDF.

## 📋 Tính năng

- ✅ Trích xuất từ một file PDF
- ✅ Batch extract từ tất cả PDF trong thư mục
- ✅ Hỗ trợ nhiều định dạng PDF:
  - Text-based
  - Table-based
  - Mixed layout
- ✅ Export sang JSON hoặc CSV
- ✅ Tự động phát hiện đáp án chính xác
- ✅ Fuzzy matching cho khả năng nhận diện cao
- ✅ Thống kê chi tiết

## 🚀 Cài đặt

### 1. Cài đặt dependencies

```bash
cd pdf_extractor
pip install -r requirements.txt
```

### 2. Chuẩn bị file PDF

Đặt tất cả file PDF cần xử lý trong workspace root hoặc bất kỳ thư mục nào

## 🎮 Cách sử dụng

### Option 1: Dòng lệnh (CLI)

```bash
cd pdf_extractor

# Trích xuất từ một file
python cli.py extract ../Chapter_1.pdf -o output.json

# Trích xuất từ tất cả PDF trong thư mục
python cli.py batch .. -o ./output

# Với phương pháp advanced (chính xác hơn)
python cli.py batch .. --advanced -o ./output

# Xem thống kê
python cli.py stats output/questions.json
```

### Option 2: Python script trực tiếp

```python
from extract_pdf import extract_from_pdf, batch_extract, save_to_json

# Trích xuất từ một file
questions = extract_from_pdf('Chapter_1.pdf')
print(f"Tìm được {len(questions)} câu hỏi")

# Batch extract
results = batch_extract('.')  # Thư mục hiện tại
save_to_json(results, 'questions.json')
```

### Option 3: Python script (Advanced)

```python
from advanced_extractor import batch_extract_advanced

results = batch_extract_advanced('.')
# Tự động phát hiện định dạng PDF tốt nhất
```

## 📊 Output Format

### JSON Format
```json
{
  "Chapter_1.pdf": [
    {
      "question": "Câu hỏi nội dung?",
      "options": {
        "a": "Phương án A",
        "b": "Phương án B",
        "c": "Phương án C",
        "d": "Phương án D"
      },
      "correct_answer": "c"
    }
  ]
}
```

### CSV Format
| File | Câu | Câu hỏi | Phương án A | Phương án B | Phương án C | Phương án D | Đáp án |
|------|-----|--------|-----------|-----------|-----------|-----------|--------|
| Chapter_1.pdf | 1 | Câu hỏi 1? | Phương án... | ... | ... | ... | C |

## 🔧 Cấu hình

### Hỗ trợ định dạng câu hỏi

Tool hỗ trợ các định dạng phổ biến:

```
# Format 1: Với "Câu X:"
Câu 1: Nội dung câu hỏi?
a) Phương án A
b) Phương án B
c) Phương án C
d) Phương án D
Đáp án: C

# Format 2: Với số thứ tự
1. Nội dung câu hỏi?
(a) Phương án A
(b) Phương án B
(c) Phương án C
(d) Phương án D
ĐA: B

# Format 3: Table format
| Câu hỏi | A | B | C | D | Đáp án |
|--------|---|---|---|---|--------|
| ... | ... | ... | ... | ... | C |
```

## 📁 Thư mục cấu trúc

```
pdf_extractor/
├── requirements.txt           # Dependencies
├── extract_pdf.py             # Basic extractor
├── advanced_extractor.py      # Advanced extractor
├── cli.py                      # CLI tool
├── README.md                   # Hướng dẫn này
└── output/
    ├── questions.json          # Kết quả JSON
    ├── questions.csv           # Kết quả CSV
    └── advanced_extraction.json # Kết quả advanced
```

## 💡 Ví dụ sử dụng

### Ví dụ 1: Extract từ một file

```bash
python cli.py extract ../Chapter_1.pdf -o results.json
```

Output:
```
📄 Đang xử lý: Chapter_1.pdf...
✅ Tìm được 25 câu hỏi

Câu 1: Đây là nội dung câu hỏi thứ nhất?
  a. Phương án A
  b. Phương án B
  c. Phương án C ✓
  d. Phương án D

...

💾 Lưu: results.json
```

### Ví dụ 2: Batch extract

```bash
python cli.py batch .. -o ./output
```

Output:
```
📁 Xử lý thư mục: ..
Tìm kiếm file PDF...

┌──────────────────────────────────────┬───────────┐
│ File PDF                             │ Số câu hỏi │
├──────────────────────────────────────┼───────────┤
│ Chapter_1.pdf                        │    25     │
│ Chapter_2.pdf                        │    30     │
│ Chapter_3.pdf                        │    20     │
└──────────────────────────────────────┴───────────┘

📊 Thống kê:
  📁 Tổng file: 3
  ❓ Tổng câu hỏi: 75

💾 Lưu: ./output
```

### Ví dụ 3: Sử dụng trong code

```python
from advanced_extractor import AdvancedPDFExtractor

# Extract từ một file
extractor = AdvancedPDFExtractor('Chapter_1.pdf')
result = extractor.extract()

print(f"Phương pháp: {result['method']}")
print(f"Tất cả: {result['total']} câu hỏi")

for q in result['questions']:
    print(f"Q: {q['question']}")
    print(f"Đáp án: {q['correct_answer']}")

extractor.close()
```

## 🔍 Chi tiết kỹ thuật

### Phương pháp trích xuất

#### 1. Text-Based (mặc định)
- Tìm pattern câu hỏi sử dụng regex
- Phân tích text tuần tự
- Nhanh nhất, phù hợp với hầu hết PDF

#### 2. Table-Based
- Trích xuất bảng từ PDF
- Dùng pdfplumber
- Tốt cho quiz format table

#### 3. Layout-Based
- Phân tích vị trí kiểu layout
- Nhóm text theo vị trí Y-coordinate
- Chính xác nhất cho layout phức tạp

### Fuzzy Matching
- Tự động match phương án chính xác
- Xử lý biến thể chỉnh tả
- Lọc bỏ trùng lặp

## ⚠️ Limitations

- Không hỗ trợ PDF scan/hình ảnh (cần OCR)
- Chính xác tùy vào format PDF
- Có thể cần tune parameters cho định dạng lạ

## 🐛 Troubleshooting

### Không tìm được câu hỏi
```bash
# Thử phương pháp advanced
python cli.py batch . --advanced
```

### Lỗi "module not found"
```bash
# Cài lại dependencies
pip install -r requirements.txt --upgrade
```

### Đáp án không chính xác
- Kiểm tra format PDF
- Xem file element.txt để hiểu cấu trúc
- Có thể sửa regex pattern trong code

## 📝 License

MIT

## 🤝 Contributing

Nếu bạn cải thiện được tool này, hãy pull request!

---

**Made with ❤️ for quiz lovers**
