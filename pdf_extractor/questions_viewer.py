#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Questions Viewer & Manager
Xem, lọc và quản lý đề thi
"""

import json
import csv
from pathlib import Path
from typing import Optional
import sys


class QuestionManager:
    """Quản lý câu hỏi"""
    
    def __init__(self, json_file: str):
        self.json_file = json_file
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def get_total_questions(self) -> int:
        """Tổng số câu hỏi"""
        return sum(len(q) for q in self.data.values())
    
    def get_file_stats(self):
        """Thống kê từng file"""
        stats = []
        for filename, questions in self.data.items():
            stats.append({
                'file': filename,
                'total': len(questions),
                'with_answer': sum(1 for q in questions if q.get('correct_answer'))
            })
        return stats
    
    def view_question(self, file_idx: int, q_idx: int):
        """Xem một câu hỏi"""
        files = sorted(self.data.keys())
        if file_idx < 0 or file_idx >= len(files):
            print("❌ File index không hợp lệ")
            return
        
        filename = files[file_idx]
        questions = self.data[filename]
        
        if q_idx < 0 or q_idx >= len(questions):
            print("❌ Question index không hợp lệ")
            return
        
        q = questions[q_idx]
        
        print(f"\n{'='*80}")
        print(f"📄 {filename}")
        print(f"{'='*80}\n")
        print(f"Câu {q['number']}: {q['question']}\n")
        
        for key in ['a', 'b', 'c', 'd']:
            if q['options'][key]:
                mark = " ✓" if q['correct_answer'] == key else ""
                print(f"  {key}. {q['options'][key]}{mark}")
        
        print(f"\nĐáp án: {(q['correct_answer'] or '?').upper()}")
        print(f"Trạng thái: {q.get('status', 'N/A')}")
        print(f"{'='*80}\n")


def main_menu():
    """Menu chính"""
    json_file = Path(__file__).parent / 'output' / 'questions.json'
    
    if not json_file.exists():
        print("❌ Không tìm thấy questions.json")
        print("Vui lòng chạy final_extractor.py trước")
        return
    
    manager = QuestionManager(str(json_file))
    
    while True:
        print("\n" + "="*80)
        print("🎯 Questions Manager")
        print("="*80)
        print(f"\n📊 Thống kê chung:")
        print(f"  Tổng câu hỏi: {manager.get_total_questions()}")
        
        print(f"\n📁 Các file:")
        files = sorted(manager.data.keys())
        for i, filename in enumerate(files):
            q_count = len(manager.data[filename])
            print(f"  {i}. {filename:50} ({q_count} câu)")
        
        print(f"\n{'─'*80}")
        print("Options:")
        print("  v. Xem câu hỏi")
        print("  s. Xem thống kê")
        print("  e. Export sang định dạng khác")
        print("  q. Thoát")
        print(f"{'─'*80}\n")
        
        choice = input("Chọn: ").strip().lower()
        
        if choice == 'q':
            print("👋 Tạm biệt!")
            break
        elif choice == 'v':
            view_questions(manager)
        elif choice == 's':
            show_stats(manager)
        elif choice == 'e':
            export_questions(manager)


def view_questions(manager: QuestionManager):
    """Xem câu hỏi"""
    files = sorted(manager.data.keys())
    
    print("\nChọn file:")
    for i, f in enumerate(files):
        print(f"  {i}. {f}")
    
    try:
        file_idx = int(input("\nFile number: "))
        filename = files[file_idx]
        questions = manager.data[filename]
        
        print(f"\nFile có {len(questions)} câu hỏi")
        print("Nhập -1 để quay lại menu")
        
        q_idx = 0
        while True:
            print(f"\nCâu {q_idx + 1}/{len(questions)}")
            q = questions[q_idx]
            
            print(f"\n❓ {q['question']}\n")
            for key in ['a', 'b', 'c', 'd']:
                if q['options'][key]:
                    print(f"  {key}. {q['options'][key]}")
            
            print(f"\n(p)revious, (n)ext, (a)nswer, (q)uit: ", end='')
            action = input().strip().lower()
            
            if action == 'q':
                break
            elif action == 'n' and q_idx < len(questions) - 1:
                q_idx += 1
            elif action == 'p' and q_idx > 0:
                q_idx -= 1
            elif action == 'a':
                print(f"✓ Đáp án: {(q['correct_answer'] or '?').upper()}")
            
    except (ValueError, IndexError):
        print("❌ Input không hợp lệ")


def show_stats(manager: QuestionManager):
    """Xem thống kê"""
    stats = manager.get_file_stats()
    
    print(f"\n{'='*80}")
    print("THỐNG KÊ CHI TIẾT")
    print(f"{'='*80}\n")
    
    total_with_answer = 0
    for stat in stats:
        per = (stat['with_answer'] / stat['total'] * 100) if stat['total'] > 0 else 0
        total_with_answer += stat['with_answer']
        print(f"✓ {stat['file']:50} {stat['total']:3} câu ({per:.0f}% có đáp án)")
    
    print(f"\n{'─'*80}")
    total = manager.get_total_questions()
    per_total = (total_with_answer / total * 100) if total > 0 else 0
    print(f"TỔNG: {total} câu ({per_total:.0f}% có đáp án)")


def export_questions(manager: QuestionManager):
    """Export dữ liệu"""
    output_dir = Path(__file__).parent / 'output'
    
    print("\nExport options:")
    print("  1. JSON (đã có)")
    print("  2. CSV với delimiter ';' (Excel compatible)")
    print("  3. TXT (dễ đọc)")
    
    choice = input("\nChọn: ")
    
    if choice == '2':
        # Export CSV with semicolon
        csv_file = output_dir / 'questions_excel.csv'
        rows = []
        
        for filename, questions in manager.data.items():
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
                }
                rows.append(row)
        
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=';')
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✓ Lưu: {csv_file}")
    
    elif choice == '3':
        # Export TXT
        txt_file = output_dir / 'questions_all.txt'
        with open(txt_file, 'w', encoding='utf-8') as f:
            for filename, questions in sorted(manager.data.items()):
                f.write(f"\n{'='*80}\n")
                f.write(f"📄 {filename}\n")
                f.write(f"{'='*80}\n\n")
                
                for i, q in enumerate(questions, 1):
                    f.write(f"Câu {i}: {q['question']}\n")
                    for key in ['a', 'b', 'c', 'd']:
                        if q['options'][key]:
                            f.write(f"  {key}. {q['options'][key]}\n")
                    f.write(f"\n")
        
        print(f"✓ Lưu: {txt_file}")
    
    else:
        print("❌ Lựa chọn không hợp lệ")


if __name__ == '__main__':
    main_menu()
