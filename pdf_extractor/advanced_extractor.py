#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced PDF Extractor - Hỗ trợ nhiều định dạng PDF khác nhau
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import re
import fitz
import pdfplumber


class AdvancedPDFExtractor:
    """
    Trích xuất câu hỏi từ PDF với hỗ trợ định dạng phức tạp
    - Table-based
    - Text-based
    - Mixed layout
    """
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc_fitz = fitz.open(pdf_path)
        self.pdf_plumber = pdfplumber.open(pdf_path)
        self.questions = []
        self.method_used = None
        
    def extract(self) -> Dict:
        """
        Trích xuất với tự động phát hiện định dạng
        """
        result = {
            'file': Path(self.pdf_path).name,
            'questions': [],
            'method': None,
            'total': 0
        }
        
        # Thử phương pháp 1: Text-based extraction
        questions = self._extract_from_text()
        if questions:
            result['questions'] = questions
            result['method'] = 'text-based'
            result['total'] = len(questions)
            return result
        
        # Thử phương pháp 2: Table-based extraction
        questions = self._extract_from_tables()
        if questions:
            result['questions'] = questions
            result['method'] = 'table-based'
            result['total'] = len(questions)
            return result
        
        # Thử phương pháp 3: Layout analysis
        questions = self._extract_from_layout()
        if questions:
            result['questions'] = questions
            result['method'] = 'layout-based'
            result['total'] = len(questions)
            return result
        
        return result
    
    def _extract_from_text(self) -> List[Dict]:
        """Trích xuất từ text thuần"""
        text = ""
        for page in self.doc_fitz:
            text += page.get_text()
        
        questions = []
        
        # Tìm các câu hỏi (pattern: Câu X, Question X, Số thứ tự)
        patterns = [
            r'Câu\s+(\d+)[:\s]+(.+?)(?=Câu\s+\d+|$)',
            r'Question\s+(\d+)[:\s]+(.+?)(?=Question\s+\d+|$)',
            r'(\d+)\.\s+(.+?)(?=\n\d+\.|$)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                block = match.group(0)
                question_obj = self._parse_block(block)
                if question_obj:
                    questions.append(question_obj)
        
        # Loại bỏ trùng lặp
        questions = self._deduplicate(questions)
        return questions
    
    def _extract_from_tables(self) -> List[Dict]:
        """Trích xuất từ bảng"""
        questions = []
        
        for page_num, page in enumerate(self.pdf_plumber.pages):
            tables = page.extract_tables()
            
            if not tables:
                continue
            
            for table in tables:
                for row in table:
                    if len(row) >= 5:  # Question + 4 options
                        question_obj = self._parse_table_row(row)
                        if question_obj:
                            questions.append(question_obj)
        
        return questions
    
    def _extract_from_layout(self) -> List[Dict]:
        """Trích xuất dựa trên layout/vị trí"""
        questions = []
        
        for page_num, page in enumerate(self.pdf_plumber.pages):
            try:
                # Thử lấy text bằng extract_text()
                text = page.extract_text()
                if text:
                    # Phân chia text theo dòng và parse
                    lines = text.split('\n')
                    for i in range(0, len(lines), 6):  # Chunk 6 lines cho một câu hỏi
                        chunk = '\n'.join(lines[i:i+6])
                        question_obj = self._parse_block(chunk)
                        if question_obj:
                            questions.append(question_obj)
            except Exception:
                continue
        
        return questions
    
    def _parse_block(self, text: str) -> Optional[Dict]:
        """Parse một block text"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if len(lines) < 5:
            return None
        
        question_obj = {
            'question': '',
            'options': {},
            'correct_answer': None,
        }
        
        # Tìm câu hỏi
        question_idx = 0
        for i, line in enumerate(lines):
            if not re.match(r'^[a-d]\)', line) and not re.match(r'^Đáp án|^ĐA:|Answer:', line):
                question_obj['question'] = line
                question_idx = i + 1
                break
        
        if not question_obj['question']:
            return None
        
        # Tìm đáp án
        options_found = 0
        for i in range(question_idx, len(lines)):
            line = lines[i]
            
            # Kiểm tra đáp án đúng
            if re.search(r'Đáp án|ĐA:|Answer:', line, re.IGNORECASE):
                match = re.search(r'[a-d]', line, re.IGNORECASE)
                if match:
                    question_obj['correct_answer'] = match.group(0).lower()
                continue
            
            # Tìm phương án (a, b, c, d)
            match = re.match(r'^([a-d])\)\s*(.+)', line)
            if match:
                option_key = match.group(1).lower()
                option_text = match.group(2)
                question_obj['options'][option_key] = option_text
                options_found += 1
        
        if question_obj['question'] and options_found >= 2:
            return question_obj
        
        return None
    
    def _parse_table_row(self, row: List) -> Optional[Dict]:
        """Parse một hàng từ bảng"""
        if len(row) < 5:
            return None
        
        question_obj = {
            'question': row[0] or '',
            'options': {
                'a': row[1] or '',
                'b': row[2] or '',
                'c': row[3] or '',
                'd': row[4] or ''
            },
            'correct_answer': row[5].lower() if len(row) > 5 else None
        }
        
        if question_obj['question']:
            return question_obj
        
        return None
    
    def _group_by_position(self, text_dict: Dict, key: str) -> List[List]:
        """Nhóm các item theo vị trí"""
        if 'text' not in text_dict:
            return []
        
        items = text_dict['text']
        groups = []
        current_group = []
        last_pos = None
        
        for item in items:
            pos = item.get(key, 0)
            if last_pos is not None and abs(pos - last_pos) > 20:
                if current_group:
                    groups.append(current_group)
                    current_group = []
            current_group.append(item)
            last_pos = pos
        
        if current_group:
            groups.append(current_group)
        
        return groups
    
    def _deduplicate(self, questions: List[Dict]) -> List[Dict]:
        """Loại bỏ câu hỏi trùng lặp"""
        seen = set()
        unique = []
        
        for q in questions:
            key = q['question'].strip()[:50]  # Use first 50 chars
            if key not in seen:
                seen.add(key)
                unique.append(q)
        
        return unique
    
    def close(self):
        """Đóng documents"""
        self.doc_fitz.close()
        self.pdf_plumber.close()


def batch_extract_advanced(pdf_dir: str) -> List[Dict]:
    """Trích xuất từ tất cả PDF với phương pháp nâng cao"""
    results = []
    pdf_path = Path(pdf_dir)
    
    for pdf_file in sorted(pdf_path.glob('*.pdf')):
        print(f"Xử lý: {pdf_file.name}...")
        try:
            extractor = AdvancedPDFExtractor(str(pdf_file))
            result = extractor.extract()
            results.append(result)
            extractor.close()
            
            if result['total'] > 0:
                print(f"  ✓ Tìm được {result['total']} câu ({result['method']})")
            else:
                print(f"  ⚠ Không tìm được câu hỏi")
        except Exception as e:
            print(f"  ✗ Lỗi: {str(e)}")
            results.append({
                'file': pdf_file.name,
                'questions': [],
                'method': 'error',
                'total': 0,
                'error': str(e)
            })
    
    return results


if __name__ == '__main__':
    workspace_root = Path(__file__).parent.parent
    results = batch_extract_advanced(str(workspace_root))
    
    output_file = workspace_root / 'pdf_extractor' / 'output' / 'advanced_extraction.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Lưu: {output_file}")
    print(f"Tổng câu hỏi: {sum(r['total'] for r in results)}")
