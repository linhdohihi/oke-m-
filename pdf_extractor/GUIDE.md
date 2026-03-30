# 🎯 PDF Questions Extractor - Complete Guide

Tool tích hợp để trích xuất, chuyển đổi và quản lý câu hỏi từ PDF quiz của LMS NEU.

## 📊 Thống kê

- ✅ **188 câu hỏi** đã trích xuất từ 13 file PDF
- 📁 Hỗ trợ Batch processing
- 🔄 Chuyển đổi PDF → TXT → JSON/CSV
- 📱 Multiple export formats

## 🚀 Cài đặt & Sử dụng

### Bước 1: Cài dependencies

```bash
cd pdf_extractor
pip install -r requirements.txt
```

### Bước 2: Chuyển PDF → TXT (Tuỳ chọn)

```bash
python pdf_to_txt.py
```

**Output:** `txt_extracted/` - Tất cả file TXT

### Bước 3: Trích xuất câu hỏi

```bash
python final_extractor.py
```

**Output:**
- `output/questions.json` - Format JSON
- `output/questions.csv` - Format CSV  
- `output/questions_readable.txt` - Dễ đọc

### Bước 4: Xem & quản lý (Optional)

```bash
python questions_viewer.py
```

Menu tương tác để:
- 📖 Xem câu hỏi
- 📊 Xem thống kê
- 💾 Export định dạng khác

## 📁 Cấu trúc thư mục

```
pdf_extractor/
├── requirements.txt
├── pdf_to_txt.py               # PDF → TXT
├── final_extractor.py          # TXT → Questions
├── questions_viewer.py         # Interactive viewer
├── README.md                   # Guide này
└── output/
    ├── questions.json          # Dữ liệu gốc
    ├── questions.csv           # CSV đơn giản
    ├── questions_excel.csv     # CSV cho Excel (;)
    ├── questions_readable.txt  # Định dạng text
    └── questions_all.txt       # Full export
```

## 📋 JSON Format

```json
{
  "Chapter_1.txt": [
    {
      "number": 1,
      "question": "Câu hỏi?",
      "options": {
        "a": "Phương án A",
        "b": "Phương án B",
        "c": "Phương án C",
        "d": "Phương án D"
      },
      "correct_answer": "a",
      "status": "Đúng"
    }
  ]
}
```

## 💻 CSV Format

| File | Câu | Câu hỏi | A | B | C | D | Đáp án | Trạng thái |
|------|-----|--------|---|---|---|---|--------|-----------|
| Chapter 1 | 1 | ... | ... | ... | ... | ... | A | Đúng |

## 🔧 Advanced Usage

### Only specific file

```bash
python final_extractor.py
# Then manipulate JSON file
```

### Custom output

Sửa `final_extractor.py` - function `save_final()`

### Merge với đáp án cũ

```python
import json

# Load existing answers
with open('data.json') as f:
    old_data = json.load(f)

# Load extracted
with open('output/questions.json') as f:
    new_data = json.load(f)

# Merge by matching questions...
```

## ⚙️ Configuration

### Change input directory

Edit `final_extractor.py`:
```python
txt_dir = Path(...)  # Your TXT directory
```

### Adjust regex patterns

Edit `final_extractor.py` - function `_extract_question()` để tuỳ chỉnh parsing

### Clean up text

Sửa regex patterns trong `_extract_question()` phần cleanup

## 📝 Log & Debug

### Check extraction result

```bash
cat output/questions_readable.txt | head -100
```

### Verify JSON

```bash
python -m json.tool output/questions.json | head -50
```

### Count questions

```bash
python -c "import json; print(sum(len(q) for q in json.load(open('output/questions.json')).values()))"
```

## 🐛 Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### "No questions extracted"
- Kiểm tra format PDF có hợp lệ
- Xem file TXT có text hay không
- Check regex pattern có matching không

### "Questions have no answer"
- Dữ liệu hiện tại không có đáp án
- Cần merge từ `data.json`
- Hoặc input đáp án thủ công vào JSON

### CSV mở không đúng trong Excel
- Dùng file `questions_excel.csv` thay vì `questions.csv`
- Hoặc import với delimiter = `;`

## 📚 Các file trong repo

### Core Tools
- `pdf_to_txt.py` - PDF conversion
- `final_extractor.py` - Extraction engine
- `questions_viewer.py` - Viewer UI

### Older (reference)
- `extract_pdf.py` - Basic extractor
- `smart_extractor.py` - Smart methods
- `advanced_extractor.py` - Advanced parsing
- `lms_extractor.py` - LMS-specific
- `txt_extractor.py` - Text extraction

## 💡 Tips

1. **Batch Processing**: Tool tự động xử lý tất cả file
2. **Flexibility**: Dễ dàng tuỳ chỉnh regex patterns
3. **Quality**: Text đã được clean up tự động
4. **Extensibility**: Dễ thêm features mới

## 🤝 Contributing

Để cải thiện tool:
1. Test với các format PDF khác
2. Tối ưu regex patterns
3. Thêm support format mới
4. Pull request lên GitHub

## 📞 Support

- Kiểm tra README này
- Debug bằng log files
- Review source code comments
- Test manual với sample data

---

**Made with ❤️ for LMS quiz extraction**

Last Updated: March 2026
