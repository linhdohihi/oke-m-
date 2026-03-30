# 🎯 PDF Questions Extractor - Summary

## ✅ Hoàn thành

Đã tạo **complete tool** để trích xuất câu hỏi từ PDF quiz:

### 📊 Kết quả Trích Xuất

- ✅ **188 câu hỏi** từ 13 file PDF
- ✅ **100% PDF files** được convert sang TXT
- ✅ Dữ liệu **sạch sẽ** (loại bỏ URL, timestamps)
- ✅ Export sang **3 format**: JSON, CSV, TXT

### 📁 Tools được tạo

1. **pdf_to_txt.py** - Chuyển PDF → TXT (gọi từ pdf_to_json.py)
   - Input: Tất cả file PDF trong workspace
   - Output: `txt_extracted/` folder

2. **final_extractor.py** - Extract questions từ TXT ⭐ CHÍNH
   - Input: `txt_extracted/` 
   - Output: `output/questions.json`, `questions.csv`, `questions_readable.txt`
   - Format: Tối ưu cho LMS NEU quiz

3. **questions_viewer.py** - Interactive viewer
   - Xem câu hỏi từng cái
   - Export thêm định dạng
   - View statistics

4. **GUIDE.md** - Hướng dẫn chi tiết
   - Setup
   - Usage
   - Troubleshooting

### 🚀 Quick Start

```bash
cd pdf_extractor

# One-liner để extract tất cả
python final_extractor.py

# Kết quả
cat output/questions.csv | head -10  # View CSV
python questions_viewer.py            # Interactive view
```

### 📋 Output Files

```
output/
├── questions.json              # Dữ liệu gốc (JSON)
├── questions.csv               # CSV format
├── questions_readable.txt      # Easy read
└── questions_excel.csv         # Excel compatible (;)
```

### 🔄 Data Flow

```
PDF Files
    ↓
pdf_to_txt.py  →  txt_extracted/
    ↓
final_extractor.py  →  output/questions.*
    ↓
questions_viewer.py  →  Interactive UI
```

### 📊 Thống kê Chi Tiết

| Metric | Value |
|--------|-------|
| Tổng file PDF | 13 |
| Tổng câu hỏi | 188 |
| Câu có đáp án | 8 (4.3%) |
| Format | ✓ JSON ✓ CSV ✓ TXT |

### 🎯 Features

- ✅ **Batch Processing** - Tất cả file một lần
- ✅ **Auto Cleanup** - Loại bỏ URL, timestamps
- ✅ **Smart Parsing** - Detect options a/b/c/d
- ✅ **Multiple Exports** - JSON, CSV, TXT
- ✅ **Interactive Viewer** - Xem từng câu
- ✅ **Well Documented** - GUIDE.md, README.md

### 💡 Cách Sử Dụng Chi Tiết

#### 1. Extract từ PDF

```bash
cd /workspaces/oke-m-/pdf_extractor
python final_extractor.py
```

Output sẽ bao gồm:
- JSON với cấu trúc: `{filename: [questions]}`
- CSV với columns: File, Câu, Câu hỏi, A, B, C, D, Đáp án, Trạng thái
- TXT dễ đọc

#### 2. View Results

```bash
# Xem CSV in terminal
cat output/questions.csv | head -5

# View JSON
python -c "import json; q=json.load(open('output/questions.json')); print(q)" | head

# Interactive viewer
python questions_viewer.py
```

#### 3. Export thêm format

```bash
python questions_viewer.py
# Chọn: e → 2 (CSV cho Excel)
```

### 🔧 Tuỳ Chỉnh

#### Thay đổi input directory

Edit `final_extractor.py`:
```python
txt_dir = Path(...)  # Your directory
```

#### Add thêm cleanup rules

Edit `_extract_question()` method:
```python
# Add regex to remove more patterns
text = re.sub(r'your_pattern', '', text)
```

#### Thay đổi output format

Sửa `save_final()` function

### 📝 Cấu Trúc JSON

```json
{
  "Chapter_1.txt": [
    {
      "number": 1,
      "question": "Câu hỏi?",
      "options": {
        "a": "Option A",
        "b": "Option B",
        "c": "Option C",
        "d": "Option D"
      },
      "correct_answer": null,
      "status": "Đúng"
    }
  ]
}
```

### ⚙️ Technology Stack

- **Language**: Python 3
- **Libraries**: 
  - `fitz` (PyMuPDF) - PDF reading
  - `csv` - CSV export
  - `json` - JSON handling
  - `re` - Regex parsing
  - `tqdm` - Progress bar

### 🎓 Học từ Code

- **Pattern Matching**: Regex patterns để parse LMS format
- **File Processing**: Batch processing PDF/TXT files
- **Data Cleaning**: Auto cleanup text content
- **CLI Design**: Interactive menu system
- **Format Conversion**: Multi-format export

### 🐛 Known Limitations

1. **Đáp án**: Chỉ tìm được 4.3% đáp án (PDF không rõ chỉ định)
   - Giải pháp: Merge với `data.json` thủ công

2. **Format**: Chỉ tối ưu cho LMS NEU
   - Giải pháp: Edit regex patterns cho format khác

3. **OCR**: Không support scan PDF/hình ảnh
   - Giải pháp: Dùng Pytesseract nếu cần

### 📚 Next Steps

1. **Add Answers**: Merge `data.json` vào questions
2. **Web UI**: Build web interface cho viewer
3. **Database**: Import vào database (SQLite/PostgreSQL)
4. **API**: Create REST API để access questions
5. **Search**: Add full-text search functionality

### 🎉 Summary

Bạn đã có:
- ✅ 188 câu hỏi struct, sạch sẽ
- ✅ 3 format export (JSON, CSV, TXT)
- ✅ Interactive viewer
- ✅ Reusable, extensible code
- ✅ Complete documentation

**Ready to use! 🚀**

---

Created: March 2026
Tools Location: `/workspaces/oke-m-/pdf_extractor/`
