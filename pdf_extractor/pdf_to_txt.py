#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert all PDF files to TXT
Chuyển đổi tất cả file PDF thành TXT
"""

import fitz
from pathlib import Path
from tqdm import tqdm


def pdf_to_txt(pdf_path: str, txt_path: str) -> bool:
    """Chuyển đổi file PDF sang TXT"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
            text += "\n" + "="*80 + "\n"  # Ngăn cách giữa các trang
        doc.close()
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"Lỗi xử lý {pdf_path}: {e}")
        return False


def batch_convert(pdf_dir: str, output_dir: str = None):
    """Chuyển đổi tất cả PDF trong thư mục"""
    pdf_dir = Path(pdf_dir)
    
    if output_dir is None:
        output_dir = pdf_dir
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_files = sorted([f for f in pdf_dir.glob('*.pdf') if not f.name.startswith('.')])
    
    print(f"\n{'='*70}")
    print(f" "*20 + "📄 PDF to TXT Converter")
    print(f"{'='*70}\n")
    print(f"📁 Thư mục input: {pdf_dir}")
    print(f"📁 Thư mục output: {output_dir}")
    print(f"📊 Tổng file: {len(pdf_files)}\n")
    
    success = 0
    failed = 0
    
    for pdf_file in tqdm(pdf_files, desc="Chuyển đổi", unit="file"):
        txt_file = output_dir / (pdf_file.stem + '.txt')
        
        if pdf_to_txt(str(pdf_file), str(txt_file)):
            success += 1
            print(f"✓ {pdf_file.name} → {txt_file.name}")
        else:
            failed += 1
            print(f"✗ {pdf_file.name}")
    
    print(f"\n{'='*70}")
    print(f"✓ Thành công: {success}")
    print(f"✗ Thất bại: {failed}")
    print(f"📁 Output: {output_dir}")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    import sys
    
    # Xác định thư mục
    workspace_root = Path(__file__).parent.parent
    txt_dir = workspace_root / 'txt_extracted'
    
    batch_convert(str(workspace_root), str(txt_dir))
