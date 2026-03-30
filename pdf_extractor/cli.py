#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Tool để sử dụng PDF Question Extractor
"""

import argparse
import json
import sys
from pathlib import Path
from tabulate import tabulate

# Import extractors
from extract_pdf import extract_from_pdf, batch_extract, save_to_json, save_to_csv
from advanced_extractor import batch_extract_advanced


def print_header():
    print("\n" + "="*70)
    print(" "*15 + "🎯 PDF Question Extractor Tool")
    print("="*70 + "\n")


def cmd_extract(args):
    """Trích xuất từ một file PDF"""
    pdf_file = Path(args.pdf)
    
    if not pdf_file.exists():
        print(f"❌ File không tồn tại: {pdf_file}")
        return
    
    print(f"📄 Đang xử lý: {pdf_file.name}...")
    
    try:
        questions = extract_from_pdf(str(pdf_file))
        
        if questions:
            print(f"✅ Tìm được {len(questions)} câu hỏi\n")
            
            # Hiển thị một số câu
            for i, q in enumerate(questions[:3], 1):
                print(f"Câu {i}: {q['question'][:80]}")
                for opt_key in ['a', 'b', 'c', 'd']:
                    opt = q['options'].get(opt_key, '')
                    mark = " ✓" if q['correct_answer'] == opt_key else ""
                    if opt:
                        print(f"  {opt_key}. {opt[:70]}{mark}")
                print()
            
            if len(questions) > 3:
                print(f"... và {len(questions) - 3} câu khác")
            
            # Lưu nếu có flag
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                if args.output.endswith('.json'):
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(questions, f, ensure_ascii=False, indent=2)
                elif args.output.endswith('.csv'):
                    data = {pdf_file.name: questions}
                    save_to_csv(data, str(output_path))
                
                print(f"\n💾 Lưu: {output_path}")
        else:
            print("⚠️  Không tìm được câu hỏi")
    
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")


def cmd_batch(args):
    """Trích xuất từ tất cả PDF trong thư mục"""
    pdf_dir = Path(args.directory)
    
    if not pdf_dir.exists():
        print(f"❌ Thư mục không tồn tại: {pdf_dir}")
        return
    
    print(f"📁 Xử lý thư mục: {pdf_dir}")
    print(f"Tìm kiếm file PDF...\n")
    
    if args.advanced:
        results = batch_extract_advanced(str(pdf_dir))
        
        # Tạo bảng thống kê
        table_data = []
        for r in results:
            table_data.append([
                r['file'],
                r['total'],
                r['method'] or 'N/A',
                r.get('error', 'OK')[:40] if r.get('error') else 'OK'
            ])
        
        print(tabulate(table_data, 
                      headers=['File', 'Câu hỏi', 'Phương pháp', 'Status'],
                      tablefmt='grid'))
    else:
        results = batch_extract(str(pdf_dir))
        
        # Tạo bảng thống kê
        table_data = []
        for filename, questions in results.items():
            table_data.append([filename, len(questions)])
        
        print(tabulate(table_data, 
                      headers=['File PDF', 'Số câu hỏi'],
                      tablefmt='grid'))
    
    # Tính tổng
    if args.advanced:
        total_questions = sum(r['total'] for r in results)
    else:
        total_questions = sum(len(q) for q in results.values())
    
    print(f"\n📊 Thống kê:")
    print(f"  📁 Tổng file: {len(results)}")
    print(f"  ❓ Tổng câu hỏi: {total_questions}")
    
    # Lưu kết quả
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if args.advanced:
            # Lưu advanced results
            results_converted = []
            for r in results:
                results_converted.append({
                    'file': r['file'],
                    'method': r['method'],
                    'total': r['total'],
                    'questions': r['questions']
                })
            json_file = output_dir / 'questions_advanced.json'
            save_to_json({'results': results_converted}, str(json_file))
        else:
            # Lưu results thường
            json_file = output_dir / 'questions.json'
            csv_file = output_dir / 'questions.csv'
            save_to_json(results, str(json_file))
            save_to_csv(results, str(csv_file))
        
        print(f"\n💾 Lưu: {output_dir}")


def cmd_stats(args):
    """Hiển thị thống kê"""
    json_file = Path(args.json)
    
    if not json_file.exists():
        print(f"❌ File không tồn tại: {json_file}")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Thống kê từ: {json_file.name}\n")
    
    if isinstance(data, dict):
        if 'results' in data:
            # Advanced format
            total_questions = sum(r['total'] for r in data['results'])
            table_data = []
            for r in data['results']:
                table_data.append([r['file'], r['total'], r['method']])
            print(tabulate(table_data, headers=['File', 'Câu hỏi', 'Phương pháp'], tablefmt='grid'))
        else:
            # Regular format
            total_questions = sum(len(q) for q in data.values())
            table_data = []
            for filename, questions in data.items():
                table_data.append([filename, len(questions)])
            print(tabulate(table_data, headers=['File PDF', 'Số câu hỏi'], tablefmt='grid'))
        
        print(f"\n📈 Kết quả:")
        print(f"  📁 Tổng file: {len(data)}")
        print(f"  ❓ Tổng câu hỏi: {total_questions}")


def main():
    parser = argparse.ArgumentParser(
        description='🎯 PDF Question Extractor Tool - Trích xuất câu hỏi từ PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  # Trích xuất từ một file
  python cli.py extract Chapter_1.pdf -o output.json
  
  # Trích xuất từ tất cả PDF trong thư mục
  python cli.py batch . -o ./output
  
  # Sử dụng phương pháp advanced
  python cli.py batch . --advanced -o ./output
  
  # Xem thống kê
  python cli.py stats output/questions.json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Lệnh')
    
    # Lệnh extract
    extract_parser = subparsers.add_parser('extract', help='Trích xuất từ một file PDF')
    extract_parser.add_argument('pdf', help='Đường dẫn file PDF')
    extract_parser.add_argument('-o', '--output', help='File output (JSON hoặc CSV)')
    extract_parser.set_defaults(func=cmd_extract)
    
    # Lệnh batch
    batch_parser = subparsers.add_parser('batch', help='Trích xuất từ tất cả PDF trong thư mục')
    batch_parser.add_argument('directory', help='Thư mục chứa PDF')
    batch_parser.add_argument('-o', '--output', help='Thư mục output')
    batch_parser.add_argument('--advanced', action='store_true', help='Sử dụng phương pháp advanced')
    batch_parser.set_defaults(func=cmd_batch)
    
    # Lệnh stats
    stats_parser = subparsers.add_parser('stats', help='Xem thống kê')
    stats_parser.add_argument('json', help='File JSON kết quả')
    stats_parser.set_defaults(func=cmd_stats)
    
    args = parser.parse_args()
    
    print_header()
    
    if not args.command:
        parser.print_help()
    else:
        args.func(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Bị hủy bởi người dùng")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
