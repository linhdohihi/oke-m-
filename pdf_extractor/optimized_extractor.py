#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimized TXT Question Extractor
Tối ưu hóa cho format TXT từ PDF LMS NEU
"""

import re
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm


class OptimizedTXTExtractor:
    """Trích xuất câu hỏi từ TXT với format tối ưu"""
    
    def __init__(self, txt_path: str):
        self.txt_path = txt_path
        with open(txt_path, 'r', encoding='utf-8') as f:
            self.text = f.read()
        self.questions = []
    
    def extract(self) -> List[Dict]:
        """Thực hiện trích xuất"""
        self.questions = self._parse_optimized_format()
        return self.questions
    
    def _parse_optimized_format(self) -> List[Dict]:
        """
        Parse format tối ưu:
        Câu hỏi N
        Đúng/Sai
        Đạt điểm X trên Y
        [Nội dung câu hỏi]
        a. [nội dung]
        b. [nội dung]
        ...
        """
        questions = []
        
        # Tách theo "Câu hỏi" + số
        parts = re.split(r'Câu\s+hỏi\s+(\d+)', self.text)
        
        # parts[0] là phần header, sau đó là những cặp (số, nội dung)
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                q_num = int(parts[i])
                q_content = parts[i + 1]
                
                question_obj = self._parse_single_question(q_content, q_num)
                if question_obj:
                    questions.append(question_obj)
        
        return questions
    
    def _parse_single_question(self, content: str, q_num: int) -> Optional[Dict]:
        """Parse một câu hỏi"""
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
            'status': None
        }
        
        idx = 0
        
        # Line 0: Status (Đúng/Sai)
        if idx < len(lines):
            status_line = lines[idx].lower()
            if 'đúng' in status_line:
                question_obj['status'] = 'Đúng'
            elif 'sai' in status_line:
                question_obj['status'] = 'Sai'
            idx += 1
        
        # Line 1: "Đạt điểm..."
        if idx < len(lines) and 'đạt điểm' in lines[idx].lower():
            idx += 1
        
        # Tìm câu hỏi (dòng không phải là option)
        while idx < len(lines):
            line = lines[idx]
            
            # Nếu không phải option, thì là câu hỏi
            if not re.match(r'^[a-d]\.\s', line):
                question_obj['question'] = line.strip()
                idx += 1
                break
            idx += 1
        
        if not question_obj['question']:
            return None
        
        # Tìm các phương án
        while idx < len(lines):
            line = lines[idx]
            
            # Match phương án: a. [nội dung]
            match = re.match(r'^([a-d])\.\s+(.*)', line)
            if match:
                option_key = match.group(1).lower()
                option_text = match.group(2).strip()
                question_obj['options'][option_key] = option_text
            
            idx += 1
        
        # Kiểm tra có đủ phương án
        options_count = sum(1 for v in question_obj['options'].values() if v)
        if options_count < 2:
            return None
        
        # Tự động detect đáp án từ dòng "Đáp án:" hoặc "ĐA:"
        # Tìm trong phần content
        if 'Đáp án' in content or 'ĐA' in content:
            answer_match = re.search(r'(?:Đáp án|ĐA)\s*[:=]?\s*([a-d])', content, re.IGNORECASE)
            if answer_match:
                question_obj['correct_answer'] = answer_match.group(1).lower()
        
        return question_obj


def batch_extract_optimized(txt_dir: str) -> Dict[str, List[Dict]]:
    """Batch extract từ tất cả file TXT"""
    results = {}
    txt_path = Path(txt_dir)
    
    txt_files = sorted([f for f in txt_path.glob('*.txt') if not f.name.startswith('.')])
    
    for txt_file in tqdm(txt_files, desc="Trích xuất", unit="file"):
        try:
            extractor = OptimizedTXTExtractor(str(txt_file))
            questions = extractor.extract()
            results[txt_file.name] = questions
        except Exception as e:
            print(f"\n❌ Lỗi {txt_file.name}: {e}")
            results[txt_file.name] = []
    
    return results


def save_results_optimized(results: Dict, output_dir: str):
    """Lưu kết quả ra nhiều format"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON - Format để dễ import
    json_file = output_dir / 'questions_extracted.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON: {json_file.name}")
    
    # CSV - Format dễ dùng
    csv_file = output_dir / 'questions_extracted.csv'
    rows = []
    
    for filename, questions in results.items():
        for q in questions:
            row = {
                'File': filename,
                'Câu': q.get('number', ''),
                'Câu hỏi': q.get('question', ''),
                'A': q.get('options', {}).get('a', ''),
                'B': q.get('options', {}).get('b', ''),
                'C': q.get('options', {}).get('c', ''),
                'D': q.get('options', {}).get('d', ''),
                'Đáp án': (q.get('correct_answer', '') or '').upper(),
                'Trạng thái': q.get('status', '')
            }
            rows.append(row)
    
    if rows:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"✓ CSV: {csv_file.name}")
    
    # TXT - Định dạng dễ đọc
    txt_file = output_dir / 'questions_extracted_readable.txt'
    with open(txt_file, 'w', encoding='utf-8') as f:
        total = 0
        for filename, questions in results.items():
            if not questions:
                continue
            
            f.write(f"\n{'='*80}\n")
            f.write(f"📄 {filename}\n")
            f.write(f"{'='*80}\n\n")
            
            for q in questions:
                f.write(f"Câu {q['number']}: {q['question']}\n")
                for key in ['a', 'b', 'c', 'd']:
                    if q['options'][key]:
                        mark = " ✓ ĐÁP ÁN" if q['correct_answer'] == key else ""
                        f.write(f"  {key}. {q['options'][key]}{mark}\n")
                f.write(f"\nĐáp án: {(q['correct_answer'] or '?').upper()} | {q.get('status', '')}\n")
                f.write("\n" + "-"*80 + "\n\n")
                total += 1
        
        f.write(f"\n{'='*80}\n")
        f.write(f"TỔNG CÂU HỎI: {total}\n")
        f.write(f"{'='*80}\n")
    
    print(f"✓ TXT: {txt_file.name}")


def print_stats_optimized(results: Dict):
    """In thống kê"""
    print("\n" + "="*80)
    print("📊 THỐNG KÊ TRÍCH XUẤT")
    print("="*80 + "\n")
    
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
    print(" "*15 + "🎯 OPTIMIZED Question Extractor")
    print("="*80 + "\n")
    
    workspace_root = Path(__file__).parent.parent
    txt_dir = workspace_root / 'txt_extracted'
    output_dir = workspace_root / 'pdf_extractor' / 'output'
    
    print(f"📁 Input: {txt_dir}\n")
    
    # Trích xuất
    results = batch_extract_optimized(str(txt_dir))
    
    # Thống kê
    print_stats_optimized(results)
    
    # Lưu kết quả
    save_results_optimized(results, str(output_dir))
    
    print(f"💾 Kết quả: {output_dir}\n")
    
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
            print(f"\nĐáp án: {(q['correct_answer'] or '?').upper()} | Trạng thái: {q.get('status', '')}")
            break


if __name__ == '__main__':
    main()
