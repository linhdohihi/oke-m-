#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Optimized Extractor
Fix format: Câu hỏi N có nội dung nằm giữa "Đạt điểm" của nó và "Câu hỏi N+1"
"""

import re
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm


class FinalExtractor:
    """Trích xuất câu hỏi - phiên bản cuối cùng"""
    
    def __init__(self, txt_path: str):
        self.txt_path = txt_path
        with open(txt_path, 'r', encoding='utf-8') as f:
            self.text = f.read()
    
    def extract(self) -> List[Dict]:
        """Thực hiện trích xuất"""
        questions = []
        
        # Split theo "Câu hỏi N"
        parts = re.split(r'Câu\s+hỏi\s+(\d+)', self.text)
        
        # Duyệt từng câu hỏi
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                q_num = int(parts[i])
                # Content của câu hỏi này bắt đầu từ sau "Câu hỏi N" 
                # cho tới trước "Câu hỏi N+1" (hoặc cuối file)
                q_content = parts[i + 1]
                
                question_obj = self._extract_question(q_content, q_num)
                if question_obj:
                    questions.append(question_obj)
        
        return questions
    
    def _extract_question(self, content: str, q_num: int) -> Optional[Dict]:
        """Extract một câu hỏi từ content"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        if len(lines) < 5:
            return None
        
        question_obj = {
            'number': q_num,
            'question': '',
            'options': {'a': None, 'b': None, 'c': None, 'd': None},
            'correct_answer': None,
            'status': None
        }
        
        idx = 0
        
        # Line 0: "Đúng" hoặc "Sai"
        if idx < len(lines):
            status_line = lines[idx].lower()
            if 'đúng' in status_line:
                question_obj['status'] = 'Đúng'
            elif 'sai' in status_line:
                question_obj['status'] = 'Sai'
            else:
                # Có thể không phải status line, bỏ qua check
                pass
            
            if question_obj['status']:
                idx += 1
        
        # Line 1: "Đạt điểm..."
        if idx < len(lines) and 'đạt điểm' in lines[idx].lower():
            idx += 1
        
        # Bây giờ tìm câu hỏi (dòng đầu tiên không phải option)
        while idx < len(lines):
            line = lines[idx]
            
            # Skip các dòng trống hoặc separator
            if not line or line.startswith('═') or line.startswith('='):
                idx += 1
                continue
            
            # Nếu không phải option pattern, đây là câu hỏi
            if not re.match(r'^[a-d][\.,\)]', line):
                question_obj['question'] = line
                idx += 1
                break
            
            idx += 1
        
        if not question_obj['question']:
            return None
        
        # Tìm các phương án (a, b, c, d)
        current_option = None
        current_text = ""
        
        while idx < len(lines):
            line = lines[idx]
            
            # Match phương án: a., b., c., d.
            option_match = re.match(r'^([a-d])[\.,\)]\s*(.*)', line)
            
            if option_match:
                # Lưu phương án trước đó nếu có
                if current_option and current_text:
                    question_obj['options'][current_option] = current_text.strip()
                
                # Bắt đầu phương án mới
                current_option = option_match.group(1).lower()
                current_text = option_match.group(2)
            elif current_option:
                # Tiếp tục nội dung phương án hiện tại
                if line and not line.startswith('═'):
                    current_text += " " + line
            
            idx += 1
        
        # Lưu phương án cuối cùng
        if current_option and current_text:
            question_obj['options'][current_option] = current_text.strip()
        
        # Kiểm tra có đủ phương án
        options_count = sum(1 for v in question_obj['options'].values() if v)
        if options_count < 2:
            return None
        
        # Tìm đáp án - look for pattern like "Đáp án: D" hoặc chỉ chữ cái
        answer_lines = '\n'.join(lines)
        answer_match = re.search(r'(?:Đáp án|ĐA|đáp án)\s*[:=]?\s*([a-d])', answer_lines, re.IGNORECASE)
        if answer_match:
            question_obj['correct_answer'] = answer_match.group(1).lower()
        
        # Clean up options - loại bỏ URL, timestamp, etc
        for key in question_obj['options']:
            if question_obj['options'][key]:
                text = question_obj['options'][key]
                # Remove URLs
                text = re.sub(r'https?://\S+', '', text)
                # Remove timestamps 
                text = re.sub(r'\d{2}:\d{2}\s+\d{1,2}/\d{1,2}/\d{2,4}', '', text)
                # Remove chapter references and page breaks
                text = re.sub(r'Chapter\s+\d+.*?(?:Quiz|Test|Mini).*?\d+/\d+\s*', '', text, flags=re.IGNORECASE)
                # Remove lines with only equals signs or dashes
                text = re.sub(r'=+|^-+$', '', text)
                # Remove "Mini Test: Xem lại lần làm thử" and similar
                text = re.sub(r'Mini Test:.*?(?=\n|$)', '', text, flags=re.IGNORECASE)
                # Clean multiple spaces and newlines
                text = ' '.join(text.split())
                question_obj['options'][key] = text.strip()
        
        # Clean question
        question_text = question_obj['question']
        question_text = re.sub(r'https?://\S+', '', question_text)
        question_text = re.sub(r'\d{2}:\d{2}\s+\d{1,2}/\d{1,2}/\d{2,4}', '', question_text)
        question_text = re.sub(r'Chapter\s+\d+.*?(?:Quiz|Test|Mini).*?\d+/\d+\s*', '', question_text, flags=re.IGNORECASE)
        question_text = re.sub(r'=+|^-+$', '', question_text)
        question_text = re.sub(r'Mini Test:.*?(?=\n|$)', '', question_text, flags=re.IGNORECASE)
        question_text = ' '.join(question_text.split())
        question_obj['question'] = question_text.strip()
        
        return question_obj


def batch_extract_final(txt_dir: str) -> Dict[str, List[Dict]]:
    """Batch extract"""
    results = {}
    txt_path = Path(txt_dir)
    txt_files = sorted([f for f in txt_path.glob('*.txt') if not f.name.startswith('.')])
    
    for txt_file in tqdm(txt_files, desc="Trích xuất", unit="file"):
        try:
            extractor = FinalExtractor(str(txt_file))
            questions = extractor.extract()
            results[txt_file.name] = questions
        except Exception as e:
            print(f"\n❌ {txt_file.name}: {e}")
            results[txt_file.name] = []
    
    return results


def save_final(results: Dict, output_dir: str):
    """Save results"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    json_file = output_dir / 'questions.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✓ {json_file.name}")
    
    # CSV
    csv_file = output_dir / 'questions.csv'
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
        print(f"✓ {csv_file.name}")
    
    # Readable TXT
    txt_file = output_dir / 'questions_readable.txt'
    with open(txt_file, 'w', encoding='utf-8') as f:
        total = 0
        for filename, questions in results.items():
            if not questions:
                continue
            
            f.write(f"\n{'='*80}\n")
            f.write(f"📄 {filename} ({len(questions)} câu)\n")
            f.write(f"{'='*80}\n\n")
            
            for q in questions:
                f.write(f"Câu {q['number']}: {q['question']}\n")
                for key in ['a', 'b', 'c', 'd']:
                    if q['options'][key]:
                        mark = " ✓" if q['correct_answer'] == key else ""
                        f.write(f"  {key}. {q['options'][key]}{mark}\n")
                f.write(f"\nĐáp án: {(q['correct_answer'] or '?').upper()}\n")
                f.write("-"*80 + "\n\n")
                total += 1
    
    print(f"✓ {txt_file.name}")
    return total


def main():
    print("\n" + "="*80)
    print(" "*20 + "🎯 FINAL Question Extractor")
    print("="*80 + "\n")
    
    workspace_root = Path(__file__).parent.parent
    txt_dir = workspace_root / 'txt_extracted'
    output_dir = workspace_root / 'pdf_extractor' / 'output'
    
    results = batch_extract_final(str(txt_dir))
    
    # Stats
    total_questions = sum(len(q) for q in results.values())
    print("\n" + "="*80)
    print(f"✓ {len(results)} file")
    print(f"✓ {total_questions} câu hỏi")
    print("="*80 + "\n")
    
    # Save
    total_saved = save_final(results, str(output_dir))
    
    print(f"\n💾 Lưu tại: {output_dir}\n")
    
    # Sample
    for filename, questions in results.items():
        if questions:
            print(f"📝 Mẫu từ {filename}:\n")
            q = questions[0]
            print(f"Câu {q['number']}: {q['question']}")
            for key in ['a', 'b', 'c', 'd']:
                if q['options'][key]:
                    mark = " ✓" if q['correct_answer'] == key else ""
                    print(f"  {key}. {q['options'][key]}{mark}")
            print(f"\nĐáp án: {(q['correct_answer'] or '?').upper()}")
            break


if __name__ == '__main__':
    main()
