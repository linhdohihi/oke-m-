import json
import re

def extract_quiz_from_raw(file_path, output_json):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    quiz_data = {}
    i = 0
    
    while i < len(lines):
        line = lines[i]

        # 1. Bỏ qua các dòng tiêu đề "Câu hỏi X" và Metadata điểm số
        if re.match(r'^Câu hỏi \d+$', line) or "Đạt điểm" in line or "Đúng" in line or "Sai" in line:
            i += 1
            continue
            
        # 2. Nhận diện Câu hỏi: Là dòng kết thúc bằng '?' hoặc ':'
        # và không phải là các lựa chọn a., b., c., d.
        if (line.endswith('?') or line.endswith(':')) and not re.match(r'^[a-d]\.', line):
            current_question = line
            correct_answer = ""
            
            # 3. Quét các dòng tiếp theo để tìm 4 lựa chọn và đáp án có dấu 
            j = i + 1
            options_count = 0
            while j < len(lines) and options_count < 4:
                # Tìm dòng bắt đầu bằng a. b. c. d.
                if re.match(r'^[a-d]\.$', lines[j]):
                    options_count += 1
                    # Nội dung đáp án thường nằm ở dòng ngay sau a. b. c. d.
                    ans_content = lines[j+1] if j+1 < len(lines) else ""
                    
                    # Kiểm tra xem dấu  nằm ở đâu (có thể cùng dòng hoặc dòng sau)
                    if "" in ans_content or (j+2 < len(lines) and "" in lines[j+2]):
                        correct_answer = ans_content.replace("", "").strip()
                    j += 2
                else:
                    # Xử lý trường hợp câu hỏi bị ngắt dòng giữa trang
                    if options_count == 0 and not "Chapter 7" in lines[j]:
                        current_question += " " + lines[j]
                    j += 1
            
            if current_question and correct_answer:
                clean_q = " ".join(current_question.split())
                clean_a = " ".join(correct_answer.split())
                quiz_data[clean_q] = clean_a
                i = j - 1 # Nhảy index đến hết câu này
        
        i += 1

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Đã trích xuất thành công {len(quiz_data)} câu hỏi.")

extract_quiz_from_raw("raw_content.txt", "data_final.json")