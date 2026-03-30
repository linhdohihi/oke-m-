import fitz  # PyMuPDF
import json
import re

def clean_text(text):
    return " ".join(text.split())

def solve_neu_pdf(pdf_path, output_json):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        # Lấy text và gộp lại để xử lý các câu bị ngắt trang
        full_text += page.get_text() + "\n"

    # 1. Tách khối dựa trên "Câu hỏi [số]"
    # Dùng regex để chia nhỏ file thành từng câu
    blocks = re.split(r'Câu hỏi\s+\d+', full_text)
    
    quiz_data = {}

    for block in blocks:
        if "Đạt điểm" not in block: # Bỏ qua phần header/footer
            continue
            
        # 2. Tìm câu hỏi
        # Câu hỏi nằm sau "Đạt điểm... trên 1,00" và trước các lựa chọn a, b, c, d
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        
        q_start = -1
        first_opt_idx = -1
        
        for i, line in enumerate(lines):
            if "Đạt điểm" in line:
                q_start = i + 1
            if re.match(r'^[a-d][\.,]', line.lower()) and first_opt_idx == -1:
                first_opt_idx = i
        
        if q_start != -1 and first_opt_idx != -1:
            # Gộp các dòng của câu hỏi (đề phòng câu hỏi dài nhiều dòng)
            raw_q = " ".join(lines[q_start:first_opt_idx])
            # Loại bỏ các từ thừa như "Đúng", "Sai", "Chapter..."
            raw_q = re.sub(r'(Chapter 8 - Part 1 - Mini Test_ Xem lại lần làm thử|Đúng|Sai)', '', raw_q)
            question_text = clean_text(raw_q)
            
            # 3. Tìm đáp án đúng bằng ký hiệu ☑
            # Vì ☑ có thể đứng một mình hoặc dính vào text, ta quét toàn bộ block
            correct_answer = ""
            
            # Tìm dòng chứa ☑
            for i, line in enumerate(lines):
                if "☑" in line:
                    # Nếu dòng đó có text luôn (ví dụ: "☑ b. Nội dung")
                    content = line.replace("☑", "").strip()
                    if len(content) > 3: # Có nội dung
                        correct_answer = re.sub(r'^[a-d][\.,]\s*', '', content)
                    else:
                        # Nếu ☑ đứng một mình, đáp án là dòng có a,b,c,d gần nó nhất (trên hoặc dưới)
                        for j in [i-1, i+1, i-2, i+2]: # Quét các dòng lân cận
                            if 0 <= j < len(lines) and re.match(r'^[a-d][\.,]', lines[j]):
                                correct_answer = re.sub(r'^[a-d][\.,]\s*', '', lines[j])
                                break
                    if correct_answer: break

            if question_text and correct_answer:
                quiz_data[question_text] = clean_text(correct_answer)

    # Xuất kết quả
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=4)

    print(f"--- Đã xong! ---")
    print(f"Tổng số câu trích xuất thành công: {len(quiz_data)}")

solve_neu_pdf("Chapter 8 - Part 1 - Mini Test_ Xem lại lần làm thử.pdf", "data.json")