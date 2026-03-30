#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Question Extractor Tool
Trích xuất câu hỏi, đáp án từ file PDF
"""

import json
import csv
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import fitz  # PyMuPDF


class PDFQuestionExtractor:
    """Trích xuất câu hỏi và đáp án từ file PDF"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.questions = []
        
    def extract_all_text(self) -> str:
        """Trích xuất toàn bộ text từ PDF"""
        text = ""
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text += page.get_text()
        return text
    
    def parse_questions(self, text: str) -> List[Dict]:
        """
        Parse text để tìm câu hỏi và đáp án
        Định dạng dự kiến:
        Câu hỏi X: [Câu hỏi nội dung]
        a. [Đáp án A]
        b. [Đáp án B]
        c. [Đáp án C]
        d. [Đáp án D]
        Đáp án: [X]
        """
        questions = []
        
        # Tách các câu hỏi
        question_blocks = re.split(r'(?:Câu hỏi\s*\d+\s*:|^|\n)(?=\d+\.|\w\))', text, flags=re.MULTILINE)
        
        for block in question_blocks:
            if not block.strip():
                continue
                
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            
            if len(lines) < 5:  # Cần ít nhất câu hỏi + 4 đáp án
                continue
            
            question_obj = self._parse_question_block(lines)
            if question_obj:
                questions.append(question_obj)
        
        return questions
    
    def _parse_question_block(self, lines: List[str]) -> Optional[Dict]:
        """Parse một block câu hỏi"""
        question_obj = {
            'question': '',
            'options': {},
            'correct_answer': None,
            'explanation': None
        }
        
        # Tìm câu hỏi (dòng đầu tiên không phải là option)
        idx = 0
        for i, line in enumerate(lines):
            if not re.match(r'^[a-d]\)\s', line) and not re.match(r'^Đáp án|^ĐA:', line):
                question_obj['question'] = line
                idx = i + 1
                break
        
        if not question_obj['question']:
            return None
        
        # Tìm các lựa chọn
        option_pattern = r'^([a-d])\)\s*(.+)'
        for i in range(idx, len(lines)):
            line = lines[i]
            
            if re.match(r'^Đáp án|^ĐA:', line):
                # Tìm đáp án đúng
                match = re.search(r'[a-d]', line)
                if match:
                    question_obj['correct_answer'] = match.group(0).lower()
                break
            
            match = re.match(option_pattern, line)
            if match:
                option_key = match.group(1).lower()
                option_text = match.group(2)
                question_obj['options'][option_key] = option_text
        
        # Kiểm tra dữ liệu hợp lệ
        if question_obj['question'] and len(question_obj['options']) >= 2:
            return question_obj
        
        return None
    
    def extract(self) -> List[Dict]:
        """Thực hiện trích xuất"""
        text = self.extract_all_text()
        self.questions = self.parse_questions(text)
        return self.questions
    
    def close(self):
        """Đóng document"""
        self.doc.close()


def extract_from_pdf(pdf_path: str) -> List[Dict]:
    """
    Hàm tiện ích để trích xuất từ một file PDF
    
    Args:
        pdf_path: Đường dẫn tới file PDF
        
    Returns:
        List các câu hỏi với đáp án
    """
    extractor = PDFQuestionExtractor(pdf_path)
    try:
        questions = extractor.extract()
        return questions
    finally:
        extractor.close()


def batch_extract(pdf_dir: str) -> Dict[str, List[Dict]]:
    """
    Trích xuất từ tất cả file PDF trong một thư mục
    
    Args:
        pdf_dir: Đường dẫn tới thư mục chứa PDF
        
    Returns:
        Dict với key là tên file, value là danh sách câu hỏi
    """
    results = {}
    pdf_path = Path(pdf_dir)
    
    for pdf_file in pdf_path.glob('*.pdf'):
        print(f"Xử lý: {pdf_file.name}...")
        try:
            questions = extract_from_pdf(str(pdf_file))
            results[pdf_file.name] = questions
            print(f"  ✓ Tìm được {len(questions)} câu hỏi")
        except Exception as e:
            print(f"  ✗ Lỗi: {str(e)}")
            results[pdf_file.name] = []
    
    return results


def save_to_json(data: Dict, output_path: str):
    """Lưu dữ liệu ra JSON"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ Lưu JSON: {output_path}")


def save_to_csv(data: Dict, output_path: str):
    """Lưu dữ liệu ra CSV"""
    all_rows = []
    
    for filename, questions in data.items():
        for idx, q in enumerate(questions, 1):
            row = {
                'File': filename,
                'Câu': idx,
                'Câu hỏi': q.get('question', ''),
                'Phương án A': q.get('options', {}).get('a', ''),
                'Phương án B': q.get('options', {}).get('b', ''),
                'Phương án C': q.get('options', {}).get('c', ''),
                'Phương án D': q.get('options', {}).get('d', ''),
                'Đáp án': q.get('correct_answer', '').upper() if q.get('correct_answer') else 'N/A'
            }
            all_rows.append(row)
    
    if all_rows:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"✓ Lưu CSV: {output_path}")
    else:
        print("✗ Không có dữ liệu để lưu")


def main():
    """Chương trình chính"""
    import sys
    
    print("=" * 60)
    print("PDF Question Extractor Tool")
    print("=" * 60)
    
    # Đường dẫn thư mục gốc
    workspace_root = Path(__file__).parent.parent
    
    # Xử lý tất cả PDF trong workspace
    results = batch_extract(str(workspace_root))
    
    # Thống kê
    total_questions = sum(len(q) for q in results.values())
    print(f"\n📊 Thống kê:")
    print(f"  - Tổng file PDF: {len(results)}")
    print(f"  - Tổng câu hỏi: {total_questions}")
    
    # Lưu kết quả
    output_dir = workspace_root / 'pdf_extractor' / 'output'
    output_dir.mkdir(exist_ok=True)
    
    save_to_json(results, str(output_dir / 'questions.json'))
    save_to_csv(results, str(output_dir / 'questions.csv'))
    
    print(f"\n✓ Hoàn thành! Kết quả lưu trong: {output_dir}")
    
    # In một số câu hỏi mẫu
    print("\n📝 Mẫu câu hỏi:")
    for filename, questions in results.items():
        if questions:
            print(f"\n{filename} ({len(questions)} câu):")
            for i, q in enumerate(questions[:2], 1):
                print(f"  Câu {i}: {q['question'][:60]}...")
            break


if __name__ == '__main__':
    main()
