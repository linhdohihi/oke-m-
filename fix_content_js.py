#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix content.js: restore logic + merge Q&A data properly
"""

import re
import json

def extract_qa_from_new(file_path):
    """Extract Q&A data from current content.js"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    qa_dict = {}
    # Match pattern: "question": "answer",
    pattern = r'"([^"]*?)":\s*"([^"]*?)"(?:,|\s*})'
    
    matches = re.finditer(pattern, content)
    for match in matches:
        q = match.group(1)
        a = match.group(2)
        # Skip broken entries
        if len(q) > 5 and len(a) > 1 and 'trong bản đồ' not in q:
            qa_dict[q] = a
    
    return qa_dict

def read_original_js(file_path):
    """Read original content.js structure"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_new_content_js(original_js, qa_dict):
    """Generate new content.js with fixed Q&A data"""
    
    # Find the qaData = { ... }; section in original
    pattern = r'const qaData = \{[^}]*?\};'
    
    # Build new qaData object
    qa_lines = ['const qaData = {']
    qa_items = list(qa_dict.items())
    
    for i, (q, a) in enumerate(qa_items):
        # Escape quotes
        q_escaped = q.replace('\\', '\\\\').replace('"', '\\"')
        a_escaped = a.replace('\\', '\\\\').replace('"', '\\"')
        
        comma = ',' if i < len(qa_items) - 1 else ''
        qa_lines.append(f'    "{q_escaped}": "{a_escaped}"{comma}')
    
    qa_lines.append('};')
    new_qa_section = '\n'.join(qa_lines)
    
    # Replace in original
    new_js = re.sub(pattern, new_qa_section, original_js, count=1, flags=re.DOTALL)
    
    return new_js

def main():
    print("=" * 60)
    print("Fixing content.js...")
    print("=" * 60)
    
    current_file = "/workspaces/oke-m-/quiz-auto-filler/content.js"
    original_file = "/tmp/content_original.js"
    output_file = "/workspaces/oke-m-/quiz-auto-filler/content_fixed.js"
    
    print("\n📂 Reading current Q&A data...")
    qa_data = extract_qa_from_new(current_file)
    print(f"✓ Extracted {len(qa_data)} valid Q&A pairs")
    
    # Show sample
    qa_sample = list(qa_data.items())[:3]
    for i, (q, a) in enumerate(qa_sample):
        print(f"\n  Sample {i+1}:")
        print(f"    Q: {q[:60]}...")
        print(f"    A: {a[:60]}...")
    
    print(f"\n📂 Reading original logic...")
    original_js = read_original_js(original_file)
    print(f"✓ Original has {len(original_js)} bytes of logic")
    
    print(f"\n✨ Merging...")
    new_js = generate_new_content_js(original_js, qa_data)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_js)
    
    print(f"✓ Saved to: {output_file}")
    print(f"✓ Total lines: {len(new_js.splitlines())}")
    
    # Verify structure
    if 'chrome.runtime.onMessage.addListener' in new_js:
        print("✓ Logic functions: ✓ PRESENT")
    if f'"{list(qa_data.keys())[0]}"' in new_js:
        print("✓ Q&A data: ✓ PRESENT")
    if 'fillAnswers()' in new_js:
        print("✓ fillAnswers function: ✓ PRESENT")
    if 'fillAllPages()' in new_js:
        print("✓ fillAllPages function: ✓ PRESENT")
    
    print(f"\n✅ Done! Apply fix:")
    print(f"   cp {output_file} {current_file}")

if __name__ == "__main__":
    main()
