#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TXT Question Extractor
Trích xuất câu hỏi từ file TXT được chuyển đổi từ PDF
"""

import re
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from tqdm import tqdm


class TXTQuestionExtractor:
    """Trích xuất câu hỏi từ file TXT"""
    
    def __init__(self, txt_path: str):
        self.txt_path = txt_path
        with open(txt_path, 'r', encoding='utf-8') as f:
            self.text = f.read()
        self.questions = []
    
    def extract(self) -> List[Dict]:
        """Thực hiện trích xuất"""
        self.questions = self._parse_text()
        return self.questions
    
    def _parse_text(self) -> List[Dict]:
        """Parse text để tìm câu hỏi"""
        questions = []
        
        # Pattern: "Câu hỏi N" hoặc "Question N"
        # Chia text theo "Câu hỏi"
        parts = re.split(r'Câu\s+hỏi\s+(\d+)', self.text)
        
        # parts[0] là phần đầu
        # Sau đó là các cặp (số, nội dung)
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                q_num = parts[i]
                q_content = parts[i + 1]
                
                question_obj = self._extract_from_content(q_content, int(q_num))
                if question_obj:
                    questions.append(question_obj)
        
        return questions
    
    def _extract_from_content(self, content: str, q_num: int) -> Optional[Dict]:
        """Trích xuất từ nội dung một câu hỏi"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        if len(lines) < 5:
            return None
        
        question_obj = {
            'number': q_num,
            'question': '',
            'options': {
                'a': None,
                'b': None,
                'c': None,
                'd': None
            },
            'correct_answer': None,
            'status': None,  # "Đúng" hoặc "Sai"
        }
        
        idx = 0
        
        # Dòng 1 thường là "Đúng" hoặc "Sai"
        if idx < len(lines):
            first_line = lines[idx].lower()
            if 'đúng' in first_line:
                question_obj['status'] = 'Đúng'
                idx += 1
            elif 'sai' in first_line:
                question_obj['status'] = 'Sai'
                idx += 1
        
        # Tìm câu hỏi (dòng tiếp theo mà không phải là option)
        while idx < len(lines):
            line = lines[idx]
            
            # Nếu là option, skip đi
            if re.match(r'^[a-d]\.\s', line):
                break
            
            # Nếu là dòng "Đạt điểm" hoặc "Điểm", skip
            if re.match(r'(Đạt|Điểm|trên)', line, re.IGNORECASE):
                idx += 1
                continue
            
            # Đây là câu hỏi
            if line and line not in ['Đúng', 'Sai']:
                question_obj['question'] = line
                idx += 1
                break
            
            idx += 1
        
        if not question_obj['question']:
            return None
        
        # Tìm các phương án
        while idx < len(lines):
            line = lines[idx]
            
            # Match phương án
            match = re.match(r'^([a-d])\.\s+(.*?)$', line)
            if match:
                option_key = match.group(1).lower()
                option_text = match.group(2).strip()
                
                # Loại bỏ dòng trống hoặc dòng chỉ chứa số
                if option_text and not option_text.isdigit():
                    question_obj['options'][option_key] = option_text
            
            # Tìm đáp án chính xác
            if re.match(r'(Đáp án|ĐA):', line):
                # Tìm ký tự a-d trong dòng này
                match = re.search(r'[a-d]', line, re.IGNORECASE)
                if match:
                    question_obj['correct_answer'] = match.group(0).lower()
            
            idx += 1
        
        # Kiểm tra xem có đủ dữ liệu không
        options_count = sum(1 for v in question_obj['options'].values() if v)
        if options_count < 2:
            return None
        
        return question_obj
    
    def close(self):
        """Không cần close cho file text"""
        pass


def batch_extract_txt(txt_dir: str) -> Dict[str, List[Dict]]:
    """Trích xuất từ tất cả file TXT"""
    txt_path = Path(txt_dir)
    results = {}
    
    txt_files = sorted([f for f in txt_path.glob('*.txt') if not f.name.startswith('.')])
    
    for txt_file in tqdm(txt_files, desc="Trích xuất", unit="file"):
        try:
            extractor = TXTQuestionExtractor(str(txt_file))
            questions = extractor.extract()
            results[txt_file.name] = questions
        except Exception as e:
            print(f"❌ Lỗi {txt_file.name}: {e}")
            results[txt_file.name] = []
    
    return results


def save_to_json(data: Dict, output_path: str):
    """Lưu kết quả ra JSON"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ Lưu JSON: {output_path}")


def save_to_csv(data: Dict, output_path: str):
    """Lưu kết quả ra CSV"""
    rows = []
    
    for filename, questions in data.items():
        for q in questions:
            row = {
                'File': filename,
                'Câu': q.get('number', ''),
                'Câu hỏi': q.get('question', ''),
                'Phương án A': q.get('options', {}).get('a', ''),
                'Phương án B': q.get('options', {}).get('b', ''),
                'Phương án C': q.get('options', {}).get('c', ''),
                'Phương án D': q.get('options', {}).get('d', ''),
                'Đáp án chính xác': (q.get('correct_answer', '') or '').upper(),
                'Trạng thái': q.get('status', '')
            }
            rows.append(row)
    
    if rows:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = rows[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"✓ Lưu CSV: {output_path}")


def print_stats(data: Dict):
    """In thống kê"""
    print("\n" + "="*80)
    print("📊 THỐNG KÊ")
    print("="*80)
    
    total_questions = 0
    file_stats = []
    
    for filename, questions in data.items():
        total = len(questions)
        total_questions += total
        file_stats.append((filename, total))
    
    # In từng file
    print(f"\n📁 Kết quả trích xuất:\n")
    for filename, count in sorted(file_stats, key=lambda x: x[1], reverse=True):
        status = "✓" if count > 0 else "⚠"
        print(f"{status} {filename:55} | {count:3} câu hỏi")
    
    print(f"\n{'─'*80}")
    print(f"📊 Tổng cộng: {len(data)} file, {total_questions} câu hỏi")
    print("="*80 + "\n")


def main():
    """Chương trình chính"""
    print("\n" + "="*80)
    print(" "*25 + "🎯 TXT Question Extractor")
    print("="*80 + "\n")
    
    workspace_root = Path(__file__).parent.parent
    txt_dir = workspace_root / 'txt_extracted'
    output_dir = workspace_root / 'pdf_extractor' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Trích xuất
    print(f"📁 Thư mục input: {txt_dir}\n")
    results = batch_extract_txt(str(txt_dir))
    
    # Thống kê
    print_stats(results)
    
    # Lưu kết quả
    json_file = output_dir / 'questions_final.json'
    csv_file = output_dir / 'questions_final.csv'
    
    save_to_json(results, str(json_file))
    save_to_csv(results, str(csv_file))
    
    print(f"\n💾 Kết quả lưu tại: {output_dir}\n")
    
    # In mẫu
    for filename, questions in results.items():
        if questions:
            print(f"\n📝 Mẫu từ {filename}:\n")
            q = questions[0]
            print(f"Câu {q['number']}: {q['question']}")
            for key in ['a', 'b', 'c', 'd']:
                if q['options'][key]:
                    mark = " ✓" if q['correct_answer'] == key else ""
                    print(f"  {key}. {q['options'][key]}{mark}")
            print(f"\nĐáp án: {(q['correct_answer'] or '?').upper()}")
            print(f"Trạng thái: {q['status']}")
            break


if __name__ == '__main__':
    main()
