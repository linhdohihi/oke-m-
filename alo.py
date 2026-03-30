import re
import os
import csv

def clean_question(text):
    """Lọc sạch đề bài, bỏ qua thông tin đường dẫn và điểm số"""
    # 1. Xóa các dòng rác hệ thống NEU (Bảng điều khiển, Ngày tháng, Điểm số)
    junk_patterns = [
        r'Bảng Điều khiển /.*?\n',
        r'Bắt đầu vào lúc.*?\n',
        r'Trạng thái.*?\n',
        r'Kết thúc lúc.*?\n',
        r'Thời gian thực hiện.*?\n',
        r'Điểm.*?\n',
        r'Câu hỏi \d+.*?\n',
        r'Đúng\n|Sai\n',
        r'https?://\S+',
        r'\d+/\d+' # Xóa số trang 1/14
    ]
    for p in junk_patterns:
        text = re.sub(p, '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 2. Xóa các lựa chọn thừa (a. b. c. d.) nếu chúng bị dính vào đề bài
    text = re.sub(r'\n[a-d]\..*', '', text, flags=re.DOTALL)
    
    # 3. Gom về 1 dòng duy nhất
    text = " ".join(text.split())
    return text.strip()

def extract_super_clean(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Tách file theo các khối đáp án "a." để nhận diện câu mới
    # Một câu thường kết thúc trước khi "a." của câu sau bắt đầu
    parts = re.split(r'\na\.\n', content)
    
    # Tìm tất cả đáp án có dấu tích  (\uf00c)
    all_lines = content.split('\n')
    correct_answers = []
    for i, line in enumerate(all_lines):
        if '' in line or '\uf00c' in line:
            # Lấy dòng nội dung phía trước dấu tích
            raw_ans = all_lines[i-1].strip() if line.strip() in ['', '\uf00c'] else line
            # Làm sạch đáp án (xóa dấu tích và ký tự a. b. c. d.)
            clean_ans = re.sub(r'^[a-d]\.\s*||\uf00c', '', raw_ans).strip()
            correct_answers.append(clean_ans)

    results = []
    # Khối đầu tiên là rác, ta xét từ khối thứ 2
    for i in range(1, len(parts)):
        if i-1 < len(correct_answers):
            # Lấy đề bài: là phần văn bản cuối cùng của khối trước đó
            # Cắt bỏ phần phân trang ========== nếu có
            raw_q = parts[i-1].split('====')[-1]
            q_final = clean_question(raw_q)
            
            if len(q_final) > 10: # Tránh lấy trúng các từ vụn vặt
                results.append((q_final, correct_answers[i-1]))
    
    return results

def main():
    folder_path = './txt_extracted'
    unique_data = {}

    if not os.path.exists(folder_path):
        print("Vui lòng tạo thư mục 'txt_extracted' và bỏ file txt vào đó.")
        return

    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".txt"):
            print(f"Đang xử lý file: {filename}")
            items = extract_super_clean(os.path.join(folder_path, filename))
            for q, a in items:
                # Dùng đề bài làm Key để tự động loại bỏ trùng lặp
                if q not in unique_data:
                    unique_data[q] = a

    # Ghi file CSV - Sử dụng QUOTE_MINIMAL và UTF-16 để Excel mở đẹp luôn
    output = "Ngan_Hang_QTTT_Chuan_NEU.csv"
    with open(output, 'w', newline='', encoding='utf-16') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Câu hỏi', 'Đáp án đúng'])
        for q, a in unique_data.items():
            writer.writerow([q, a])

    print(f"\n--- KẾT QUẢ ---")
    print(f"✅ Đã lọc xong: {len(unique_data)} câu hỏi duy nhất.")
    print(f"📁 File kết quả: {output}")

if __name__ == "__main__":
    main()