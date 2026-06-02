#!/usr/bin/env python3
"""
全面转义 Markdown 文件中的所有 HTML 标签
"""

import os
import re

DOCS_DIR = "/root/liyyro/docs"

def escape_all_html(content):
    """转义所有 HTML 标签"""
    lines = content.split('\n')
    result = []
    in_code_block = False
    
    for line in lines:
        # 检测围栏代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        
        if in_code_block:
            result.append(line)
            continue
        
        # 转义所有 HTML 标签
        # 匹配 <tag> 或 </tag> 或 <tag attr="value">
        # 但不匹配 Markdown 链接中的 <https://...>
        if re.search(r'<(?!https?://|/|!)[a-zA-Z][^>]*>', line):
            # 转义 < 和 > 但保留 &lt; 和 &gt;
            line = re.sub(r'<(?!https?://|/|!)([a-zA-Z][^>]*)>', r'&lt;\1&gt;', line)
        
        result.append(line)
    
    return '\n'.join(result)

def main():
    print("全面转义 HTML 标签...")
    
    fixed_count = 0
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(root, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = escape_all_html(content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed_count += 1
                print(f"已修复: {os.path.relpath(filepath, DOCS_DIR)}")
    
    print(f"\n修复完成! 共修复 {fixed_count} 个文件")

if __name__ == '__main__':
    main()
