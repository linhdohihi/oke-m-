#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Improved PDF Question Extractor
Kết hợp logic từ pdf_to_json.py và xử lý advanced
"""

import fitz
import json
import re
import csv
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm


def clean_text(text):
    """Làm sạch text"""
    return " ".join(text.split())


class SMARTQuestionExtractor:
    """Trích xuất câu hỏi sử dụng multiple strategies"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        
    def extract(self) -> List[Dict]:
        """Thực hiện trích xuất"""
        # Lấy toàn bộ text
        full_text = self._get_full_text()
        
        # Parse questions
        questions = self._parse_neu_format(full_text)
        
        return questions
    
    def _get_full_text(self) -> str:
        """Lấy toàn bộ text từ PDF"""
        text = ""
        for page in self.doc:
            text += page.get_text() + "\n"
        return text
    
    def _parse_neu_format(self, full_text: str) -> List[Dict]:
        """
        Parse NEU LMS quiz format
        Strategy:
        1. Tách khối theo "Câu hỏi N"
        2. Dùng "Đạt điểm" làm điểm mốc
        3. Dùng ☑ để tìm đáp án chính xác
        """
        questions = []
        
        # Chia thành từng câu hỏi
        blocks = re.split(r'Câu\s+hỏi\s+\d+', full_text)
        
        q_num = 0
        for block in blocks:
            if "Đạt điểm" not in block:
                continue
            
            q_num += 1
            question_obj = self._parse_block(block, q_num)
            if question_obj:
                questions.append(question_obj)
        
        return questions
    
    def _parse_block(self, block: str, q_num: int) -> Optional[Dict]:
        """Parse một block câu hỏi"""
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        
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
            'correct_answer_text': None,
        }
        
        # 1. Tìm câu hỏi (sau "Đạt điểm" và trước phương án đầu tiên)
        q_start = -1
        first_opt_idx = -1
        
        for i, line in enumerate(lines):
            if "Đạt điểm" in line:
                q_start = i + 1
            # Tìm dòng đầu tiên khớp pattern [a-d].
            if re.match(r'^[a-d][\.,]', line.lower()) and first_opt_idx == -1:
                first_opt_idx = i
        
        if q_start == -1 or first_opt_idx == -1:
            return None
        
        # Gộp các dòng câu hỏi
        raw_q = " ".join(lines[q_start:first_opt_idx])
        # Loại bỏ từ thừa
        raw_q = re.sub(r'(Chapter \d+.*?Mini Test|Đúng|Sai)', '', raw_q, flags=re.IGNORECASE)
        question_text = clean_text(raw_q)
        
        if not question_text:
            return None
        
        question_obj['question'] = question_text
        
        # 2. Tìm các phương án
        for i in range(first_opt_idx, len(lines)):
            line = lines[i]
            
            # Match pattern [a-d]. [text]
            match = re.match(r'^([a-d])[\.,]\s*(.*)', line)
            if match:
                option_key = match.group(1).lower()
                option_text = clean_text(match.group(2))
                question_obj['options'][option_key] = option_text
        
        # 3. Tìm đáp án chính xác dùng ☑
        for i, line in enumerate(lines):
            if "☑" in line:
                # Xứ lý dòng chứa ☑
                content = line.replace("☑", "").strip()
                
                if len(content) > 3:
                    # ☑ dính vào text
                    match = re.match(r'^([a-d])[\.,]?\s*(.*)', content)
                    if match:
                        answer_key = match.group(1).lower()
                        answer_text = clean_text(match.group(2))
                        question_obj['correct_answer'] = answer_key
                        question_obj['correct_answer_text'] = answer_text
                else:
                    # ☑ đứng một mình, tìm dòng gần nhất
                    for j in [i-1, i+1, i-2, i+2]:
                        if 0 <= j < len(lines):
                            match = re.match(r'^([a-d])[\.,]\s*(.*)', lines[j])
                            if match:
                                answer_key = match.group(1).lower()
                                answer_text = clean_text(match.group(2))
                                question_obj['correct_answer'] = answer_key
                                question_obj['correct_answer_text'] = answer_text
                                break
                break
        
        # Kiểm tra dữ liệu hợp lệ
        if question_obj['question'] and question_obj['correct_answer']:
            return question_obj
        
        return None
    
    def close(self):
        """Đóng document"""
        self.doc.close()


def batch_extract_smart(pdf_dir: str) -> Dict[str, List[Dict]]:
    """Batch extract từ tất cả PDF"""
    results = {}
    pdf_path = Path(pdf_dir)
    
    pdf_files = sorted([f for f in pdf_path.glob('*.pdf') if not f.name.startswith('.')])
    
    for pdf_file in tqdm(pdf_files, desc="Trích xuất", unit="file"):
        try:
            extractor = SMARTQuestionExtractor(str(pdf_file))
            questions = extractor.extract()
            results[pdf_file.name] = questions
            extractor.close()
        except Exception as e:
            print(f"\n❌ Lỗi {pdf_file.name}: {e}")
            results[pdf_file.name] = []
    
    return results


def save_results(results: Dict, output_dir: str):
    """Lưu kết quả ra nhiều format"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    json_file = output_dir / 'questions_extracted.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON: {json_file}")
    
    # CSV
    csv_file = output_dir / 'questions_extracted.csv'
    rows = []
    
    for filename, questions in results.items():
        for q in questions:
            row = {
                'File': filename,
                'Câu': q.get('number', ''),
                'Câu hỏi': q.get('question', ''),
                'Phương án A': q.get('options', {}).get('a', ''),
                'Phương án B': q.get('options', {}).get('b', ''),
                'Phương án C': q.get('options', {}).get('c', ''),
                'Phương án D': q.get('options', {}).get('d', ''),
                'Đáp án': (q.get('correct_answer', '') or '').upper(),
                'Nội dung đáp án': q.get('correct_answer_text', '')
            }
            rows.append(row)
    
    if rows:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"✓ CSV: {csv_file}")
    
    # TXT (simple format)
    txt_file = output_dir / 'questions_extracted.txt'
    with open(txt_file, 'w', encoding='utf-8') as f:
        for filename, questions in results.items():
            f.write(f"\n{'='*80}\n")
            f.write(f"📄 {filename}\n")
            f.write(f"{'='*80}\n\n")
            
            for q in questions:
                f.write(f"Câu {q['number']}: {q['question']}\n")
                for key in ['a', 'b', 'c', 'd']:
                    if q['options'][key]:
                        mark = " ✓ ĐÁP ÁN" if q['correct_answer'] == key else ""
                        f.write(f"  {key}. {q['options'][key]}{mark}\n")
                f.write("\n")
    print(f"✓ TXT: {txt_file}")


def print_stats(results: Dict):
    """In thống kê"""
    print("\n" + "="*80)
    print("📊 THỐNG KÊ KẾT QUẢ")
    print("="*80)
    
    total_questions = 0
    
    for filename, questions in sorted(results.items()):
        total = len(questions)
        total_questions += total
        status = "✓" if total > 0 else "⚠"
        print(f"{status} {filename:55} | {total:3} câu")
    
    print(f"\n{'─'*80}")
    print(f"📊 Tổng: {len(results)} file, {total_questions} câu hỏi")
    print("="*80 + "\n")


def main():
    """Chương trình chính"""
    print("\n" + "="*80)
    print(" "*20 + "🎯 SMART Question Extractor")
    print("="*80 + "\n")
    
    workspace_root = Path(__file__).parent.parent
    output_dir = workspace_root / 'pdf_extractor' / 'output'
    
    print(f"📁 Thư mục input: {workspace_root}\n")
    
    # Trích xuất
    results = batch_extract_smart(str(workspace_root))
    
    # Thống kê
    print_stats(results)
    
    # Lưu kết quả
    save_results(results, str(output_dir))
    
    print(f"\n💾 Kết quả lưu tại: {output_dir}\n")
    
    # In mẫu
    for filename, questions in results.items():
        if questions and len(questions) > 0:
            print(f"\n📝 Mẫu từ {filename}:\n")
            q = questions[0]
            print(f"Câu {q['number']}: {q['question']}")
            for key in ['a', 'b', 'c', 'd']:
                if q['options'][key]:
                    mark = " ✓" if q['correct_answer'] == key else ""
                    print(f"  {key}. {q['options'][key]}{mark}")
            print(f"\nĐáp án: {(q['correct_answer'] or '?').upper()} - {q.get('correct_answer_text', '')}")
            break


if __name__ == '__main__':
    main()
