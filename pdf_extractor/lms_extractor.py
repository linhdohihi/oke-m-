#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LMS Quiz Format Extractor
Tối ưu hóa để trích xuất từ PDF quiz của LMS NEU
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
import fitz


class LMSQuizExtractor:
    """Trích xuất câu hỏi từ PDF quiz của LMS NEU"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.questions = []
        
    def extract(self) -> List[Dict]:
        """Thực hiện trích xuất"""
        # Trích xuất đầy đủ text từ PDF
        full_text = self._get_full_text()
        
        # Parse questions
        questions = self._parse_lms_format(full_text)
        
        return questions
    
    def _get_full_text(self) -> str:
        """Lấy toàn bộ text từ PDF"""
        text = ""
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text += page.get_text() + "\n"
        return text
    
    def _parse_lms_format(self, text: str) -> List[Dict]:
        """
        Parse format LMS quiz
        Pattern:
        Câu hỏi N
        Đúng/Sai
        [Question text]
        a. [option]
        b. [option]
        c. [option]
        d. [option]
        """
        questions = []
        
        # Tách các phần "Câu hỏi" từ text
        # Pattern: "Câu hỏi \d+" hoặc "Question \d+"
        question_pattern = r'Câu\s+hỏi\s+(\d+)'
        
        sections = re.split(question_pattern, text)
        
        # sections[0] là phần đầu, sau đó là các cặp (number, content)
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                q_num = sections[i]
                q_content = sections[i + 1]
                
                question_obj = self._parse_question_section(q_content, int(q_num))
                if question_obj:
                    questions.append(question_obj)
        
        return questions
    
    def _parse_question_section(self, content: str, q_num: int) -> Optional[Dict]:
        """Parse một section của một câu hỏi"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        if len(lines) < 2:
            return None
        
        question_obj = {
            'number': q_num,
            'question': '',
            'options': {},
            'correct_answer': None,
            'is_correct': None,
        }
        
        idx = 0
        
        # Dòng đầu tiên thường là "Đúng" hoặc "Sai"
        first_line = lines[0].lower()
        if 'đúng' in first_line:
            question_obj['is_correct'] = True
            idx = 1
        elif 'sai' in first_line:
            question_obj['is_correct'] = False
            idx = 1
        
        # Tìm câu hỏi (dòng tiếp theo không phải là option)
        while idx < len(lines):
            line = lines[idx]
            if not re.match(r'^[a-d]\.\s', line, re.IGNORECASE):
                question_obj['question'] = line
                idx += 1
                break
            idx += 1
        
        if not question_obj['question']:
            return None
        
        # Tìm các phương án
        while idx < len(lines):
            line = lines[idx]
            
            # Match phương án (a., b., c., d.)
            match = re.match(r'^([a-d])\.\s*(.+)', line)
            if match:
                option_key = match.group(1).lower()
                option_text = match.group(2)
                question_obj['options'][option_key] = option_text
            
            idx += 1
        
        # Phải có ít nhất 2 phương án
        if len(question_obj['options']) < 2:
            return None
        
        return question_obj
    
    def close(self):
        """Đóng document"""
        self.doc.close()


def extract_from_lms_pdf(pdf_path: str) -> Dict:
    """
    Hàm tiện ích để trích xuất từ LMS PDF
    """
    extractor = LMSQuizExtractor(pdf_path)
    try:
        questions = extractor.extract()
        return {
            'file': Path(pdf_path).name,
            'total': len(questions),
            'questions': questions
        }
    finally:
        extractor.close()


def batch_extract_lms(pdf_dir: str) -> Dict:
    """Trích xuất từ tất cả PDF"""
    results = {}
    pdf_path = Path(pdf_dir)
    
    for pdf_file in sorted(pdf_path.glob('*.pdf')):
        if pdf_file.name.startswith('.'):
            continue
        
        print(f"Xử lý: {pdf_file.name}...", end=' ')
        try:
            result = extract_from_lms_pdf(str(pdf_file))
            results[pdf_file.name] = result['questions']
            print(f"✓ {result['total']} câu hỏi")
        except Exception as e:
            print(f"✗ Lỗi: {str(e)}")
            results[pdf_file.name] = []
    
    return results


if __name__ == '__main__':
    import sys
    
    print("\n" + "="*60)
    print(" "*15 + "LMS Quiz Extractor")
    print("="*60 + "\n")
    
    workspace_root = Path(__file__).parent.parent
    
    results = batch_extract_lms(str(workspace_root))
    
    # Statistics
    total_questions = sum(len(q) for q in results.values())
    print(f"\n📊 Thống kê:")
    print(f"  📁 Tổng file: {len(results)}")
    print(f"  ❓ Tổng câu hỏi: {total_questions}")
    
    # Lưu kết quả
    output_dir = workspace_root / 'pdf_extractor' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    json_file = output_dir / 'questions_lms.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Lưu: {json_file}")
    
    # In mẫu
    print(f"\n📝 Mẫu câu hỏi:")
    for filename, questions in results.items():
        if questions:
            print(f"\n{filename} ({len(questions)} câu):")
            for q in questions[:2]:
                print(f"  {q['question'][:60]}...")
            break
