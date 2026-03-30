#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge CSV data into LMS quiz auto-filler tool
Converts Ngan_Hang_QTTT_Chuan_NEU.csv and adds to quiz-auto-filler/content.js
"""

import csv
import json
import re
from pathlib import Path
from collections import defaultdict

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    # Remove metadata like "Đạt Đạt", timestamps, etc.
    text = re.sub(r'Đạt\s+', '', text)
    text = re.sub(r'\d{1,2}:\d{2}\s+\d{1,2}/\d{1,2}/\d{2}', '', text)
    text = re.sub(r'Wednesday|Monday|Tuesday|Thursday|Friday|Saturday|Sunday', '', text, flags=re.IGNORECASE)
    text = re.sub(r'AM|PM', '', text)
    text = re.sub(r'Thời gian thực hiện.*?giây', '', text, flags=re.DOTALL)
    text = re.sub(r'trên\s+\d+,\d+\s*\(.*?\)', '', text)
    text = re.sub(r'Đã xong', '', text)
    text = re.sub(r'Mini Test|Xem lại lần làm thử', '', text)
    text = re.sub(r'Chapter\s+\d+.*?Management', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Week\s+\d+', '', text)
    text = re.sub(r'Part\s+\d+', '', text)
    text = re.sub(r'/\s+', '/', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_csv(csv_file):
    """Parse CSV file and extract Q&A pairs"""
    qa_pairs = {}
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        # Read as tab-separated or comma-separated
        reader = csv.reader(f, delimiter='\t')
        
        for i, row in enumerate(reader):
            if i == 0:  # Skip header
                continue
            
            if len(row) >= 2:
                question = clean_text(row[0])
                answer = clean_text(row[1])
                
                # Only add if both question and answer are meaningful
                if question and answer and len(question) > 10 and len(answer) > 2:
                    qa_pairs[question] = answer
    
    return qa_pairs

def read_existing_content_js(js_file):
    """Extract existing Q&A data from content.js"""
    existing = {}
    
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract qaData object - look for pattern: "question": "answer",
    pattern = r'"([^"]+)":\s*"([^"]+)"'
    matches = re.findall(pattern, content)
    
    for question, answer in matches:
        existing[question] = answer
    
    return existing

def merge_qa_data(existing, new):
    """Merge new Q&A pairs with existing ones, avoiding duplicates"""
    merged = existing.copy()
    added_count = 0
    
    for question, answer in new.items():
        # Check if similar question already exists
        similar_found = False
        for existing_q in merged.keys():
            # Simple similarity check - if question is substring or vice versa
            if (question.lower() in existing_q.lower() or 
                existing_q.lower() in question.lower()):
                similar_found = True
                break
        
        if not similar_found:
            merged[question] = answer
            added_count += 1
    
    print(f"✓ Merged {added_count} new Q&A pairs")
    print(f"✓ Total Q&A pairs: {len(merged)}")
    
    return merged

def generate_content_js(qa_data):
    """Generate new content.js with merged Q&A data"""
    lines = [
        "// Import dữ liệu Q&A",
        "const qaData = {"
    ]
    
    # Add Q&A pairs
    qa_list = list(qa_data.items())
    for i, (question, answer) in enumerate(qa_list):
        # Escape quotes properly for JavaScript
        q_escaped = question.replace('"', '\\"')
        a_escaped = answer.replace('"', '\\"')
        
        comma = "," if i < len(qa_list) - 1 else ""
        lines.append(f'    "{q_escaped}": "{a_escaped}"{comma}')
    
    lines.append("};")
    
    return "\n".join(lines)

def main():
    print("=" * 60)
    print("LMS CSV Data Merger")
    print("=" * 60)
    
    # File paths
    csv_file = "/workspaces/oke-m-/Ngan_Hang_QTTT_Chuan_NEU.csv"
    # First convert to UTF-8
    csv_utf8 = "/tmp/Ngan_Hang_QTTT_Chuan_NEU_UTF8.csv"
    js_file = "/workspaces/oke-m-/quiz-auto-filler/content.js"
    output_file = "/workspaces/oke-m-/quiz-auto-filler/content_merged.js"
    
    print(f"\n📂 Reading CSV: {csv_file}")
    # Convert encoding first
    import subprocess
    subprocess.run(['iconv', '-f', 'UTF-16', '-t', 'UTF-8', csv_file, '-o', csv_utf8], 
                   check=True)
    
    # Parse CSV
    new_qa = parse_csv(csv_utf8)
    print(f"✓ Extracted {len(new_qa)} Q&A pairs from CSV")
    
    print(f"\n📂 Reading existing: {js_file}")
    existing_qa = read_existing_content_js(js_file)
    print(f"✓ Found {len(existing_qa)} existing Q&A pairs")
    
    print(f"\n🔄 Merging data...")
    merged_qa = merge_qa_data(existing_qa, new_qa)
    
    print(f"\n✨ Generating merged content.js...")
    new_content = generate_content_js(merged_qa)
    
    # Write to output file first
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Saved to: {output_file}")
    
    # Show sample
    print(f"\n📋 Sample (first 5 Q&A pairs):")
    for i, (q, a) in enumerate(list(merged_qa.items())[:5]):
        print(f"\n  Q{i+1}: {q[:60]}...")
        print(f"  A{i+1}: {a[:60]}...")
    
    print(f"\n✅ Done! Copy {output_file} to {js_file} when ready.")
    print(f"   Command: cp {output_file} {js_file}")

if __name__ == "__main__":
    main()
