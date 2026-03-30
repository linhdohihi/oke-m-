#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultra Optimized Extractor v2
Fix format: Câu 1, 2 metadata ở trước, nội dung nằm giữa các đoạn
"""

import re
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm


class UltraOptimizedExtractor:
    """Trích xuất smart cho LMS quad format"""
    
    def __init__(self, txt_path: str):
        self.txt_path = txt_path
        with open(txt_path, 'r', encoding='utf-8') as f:
            self.text = f.read()
    
    def extract(self) -> List[Dict]:
        """Thực hiện trích xuất"""
        # Thay vì split theo "Câu hỏi N", ta sẽ:
        # 1. Find all "Câu hỏi N" positions
        # 2. Extract content giữa các "Câu hỏi" 
        # 3. Cleanup metadata
        
        questions = []
        
        # Find all question markers with their positions
        q_pattern = r'Câu\s+hỏi\s+(\d+)'
        q_matches = list(re.finditer(q_pattern, self.text))
        
        for idx, match in enumerate(q_matches):
            q_num = int(match.group(1))
            
            # Content này bắt đầu từ sau "Câu hỏi N" 
            # và kết thúc tới trước "Câu hỏi N+1" hoặc cuối file
            start_pos = match.end()
            if idx + 1 < len(q_matches):
                end_pos = q_matches[idx + 1].start()
            else:
                end_pos = len(self.text)
            
            content = self.text[start_pos:end_pos]
            question_obj = self._parse_content(content, q_num)
            
            if question_obj:
                questions.append(question_obj)
        
        return questions
    
    def _parse_content(self, content: str, q_num: int) -> Optional[Dict]:
        """Parse content của một câu hỏi"""
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
        
        # Skip metadata lines (Đúng, Sai, Đạt điểm)
        while idx < len(lines):
            line = lines[idx].lower()
            if any(x in line for x in ['đúng', 'sai', 'đạt điểm', 'trên']):
                if 'đúng' in line:
                    question_obj['status'] = 'Đúng'
                elif 'sai' in line:
                    question_obj['status'] = 'Sai'
                idx += 1
            else:
                break
        
        # Bây giờ tìm câu hỏi thực tế
        # Câu hỏi là dòng đầu tiên không phải option pattern
        while idx < len(lines):
            line = lines[idx]
            
            # Skip separator
            if not line or line.startswith('═') or line.startswith('='):
                idx += 1
                continue
            
            # Skip "Câu hỏi N+1" nếu có
            if re.match(r'Câu\s+hỏi\s+\d+', line):
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
        
        # Tìm options
        current_option = None
        current_text = ""
        
        while idx < len(lines):
            line = lines[idx]
            
            # Match pattern [a-d].
            option_match = re.match(r'^([a-d])[\.,\)]\s*(.*)', line)
            
            if option_match:
                # Save previous option
                if current_option and current_text:
                    question_obj['options'][current_option] = current_text.strip()
                
                # Start new option
                current_option = option_match.group(1).lower()
                current_text = option_match.group(2)
            elif current_option:
                # Continue option text
                if line and not line.startswith('═'):
                    current_text += " " + line
            
            idx += 1
        
        # Save last option
        if current_option and current_text:
            question_obj['options'][current_option] = current_text.strip()
        
        # Verify enough options
        options_count = sum(1 for v in question_obj['options'].values() if v)
        if options_count < 2:
            return None
        
        # Find answer (tìm trong content)
        answer_match = re.search(r'(?:Đáp án|ĐA|đáp án)\s*[:=]?\s*([a-d])', content, re.IGNORECASE)
        if answer_match:
            question_obj['correct_answer'] = answer_match.group(1).lower()
        
        # Cleanup
        self._cleanup_text(question_obj)
        
        return question_obj
    
    def _cleanup_text(self, question_obj: Dict):
        """Clean up text"""
        # Question cleanup
        q = question_obj['question']
        q = re.sub(r'https?://\S+', '', q)
        q = re.sub(r'\d{2}:\d{2}\s+\d{1,2}/\d{1,2}/\d{2,4}', '', q)
        q = re.sub(r'Chapter\s+\d+.*?(?:Quiz|Test|Mini).*?\d+/\d+', '', q, flags=re.IGNORECASE)
        q = re.sub(r'=+', '', q)
        q = ' '.join(q.split())
        question_obj['question'] = q.strip()
        
        # Options cleanup
        for key in question_obj['options']:
            if question_obj['options'][key]:
                text = question_obj['options'][key]
                text = re.sub(r'https?://\S+', '', text)
                text = re.sub(r'\d{2}:\d{2}\s+\d{1,2}/\d{1,2}/\d{2,4}', '', text)
                text = re.sub(r'Chapter\s+\d+.*?(?:Quiz|Test|Mini).*?\d+/\d+', '', text, flags=re.IGNORECASE)
                text = re.sub(r'=+', '', text)
                text = ' '.join(text.split())
                question_obj['options'][key] = text.strip()


def batch_extract_ultra(txt_dir: str) -> Dict[str, List[Dict]]:
    """Batch extract"""
    results = {}
    txt_path = Path(txt_dir)
    txt_files = sorted([f for f in txt_path.glob('*.txt') if not f.name.startswith('.')])
    
    for txt_file in tqdm(txt_files, desc="Trích xuất", unit="file"):
        try:
            extractor = UltraOptimizedExtractor(str(txt_file))
            questions = extractor.extract()
            results[txt_file.name] = questions
        except Exception as e:
            print(f"\n❌ {txt_file.name}: {e}")
            results[txt_file.name] = []
    
    return results


def save_ultra(results: Dict, output_dir: str):
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
    print(" "*20 + "🎯 ULTRA-OPTIMIZED Question Extractor")
    print("="*80 + "\n")
    
    workspace_root = Path(__file__).parent.parent
    txt_dir = workspace_root / 'txt_extracted'
    output_dir = workspace_root / 'pdf_extractor' / 'output'
    
    results = batch_extract_ultra(str(txt_dir))
    
    # Stats
    total_questions = sum(len(q) for q in results.values())
    print("\n" + "="*80)
    print(f"✓ {len(results)} file")
    print(f"✓ {total_questions} câu hỏi")
    print("="*80 + "\n")
    
    # Save
    total_saved = save_ultra(results, str(output_dir))
    
    print(f"\n💾 Lưu tại: {output_dir}\n")
    
    # Sample
    for filename, questions in results.items():
        if questions:
            print(f"📝 Mẫu từ {filename}:\n")
            for i, q in enumerate(questions[:2], 1):
                print(f"Câu {q['number']}: {q['question'][:70]}...")
                for key in ['a', 'b', 'c', 'd']:
                    if q['options'][key]:
                        print(f"  {key}. {q['options'][key][:60]}...")
                print()
            break


if __name__ == '__main__':
    main()
