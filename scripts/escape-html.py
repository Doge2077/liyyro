#!/usr/bin/env python3
"""
转义 Markdown 文件中的 HTML 标签
避免 Vue 模板解析错误
"""

import os
import re

DOCS_DIR = "/root/liyyro/docs"

def escape_html_tags(content):
    """转义 HTML 标签"""
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
        
        # 转义 HTML 标签（但保留图片和链接）
        # 匹配 <tag> 但不匹配 <img> 或 <a>
        if re.search(r'<(?!img|a|/a|br|hr|div|/div|span|/span|p|/p|pre|/pre|code|/code|blockquote|/blockquote|ul|/ul|ol|/ol|li|/li|h[1-6]|/h[1-6]|table|/table|tr|/tr|td|/td|th|/th|thead|/thead|tbody|/tbody)[a-zA-Z][^>]*>', line):
            # 转义 < 和 >
            line = line.replace('<', '&lt;').replace('>', '&gt;')
        
        result.append(line)
    
    return '\n'.join(result)

def main():
    print("转义 HTML 标签...")
    
    fixed_count = 0
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(root, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = escape_html_tags(content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed_count += 1
                print(f"已修复: {os.path.relpath(filepath, DOCS_DIR)}")
    
    print(f"\n修复完成! 共修复 {fixed_count} 个文件")

if __name__ == '__main__':
    main()
