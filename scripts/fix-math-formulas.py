#!/usr/bin/env python3
"""
快速修复数学公式格式问题
将 "文字： $$公式$$" 格式修复为 "文字：\n\n$$公式$$"
"""

import os
import re

DOCS_DIR = "/root/liyyro/docs"

def fix_math_formulas(content):
    """修复数学公式格式"""
    lines = content.split('\n')
    result = []
    fixed_count = 0
    
    for i, line in enumerate(lines):
        # 检查是否有 "文字： $$" 或 "文字 $$" 格式
        # 模式：行首有文字，后面跟着 $$
        match = re.match(r'^(.+?)[\s]*\$\$\s*$', line)
        if match:
            text = match.group(1).strip()
            # 如果文字不是空的，说明是格式错误
            if text and not text.startswith('$$'):
                result.append(text)
                result.append('')
                result.append('$$')
                fixed_count += 1
                continue
        
        # 检查 "文字： $$公式$$" 内联格式（在同一行）
        # 这种格式是正确的，不需要修复
        # 但是如果 $$ 前面有文字且公式跨行，需要修复
        
        result.append(line)
    
    return '\n'.join(result), fixed_count


def fix_display_math_start(content):
    """修复块级数学公式的开始标记"""
    # 匹配模式：文字后面跟着 $$（可能是块级公式的开始）
    # 例如：点积定义： $$
    # 修复为：点积定义：
    # $$
    
    pattern = r'^(.+?)\s*\$\$\s*$'
    
    lines = content.split('\n')
    result = []
    fixed_count = 0
    in_math = False
    
    for line in lines:
        if not in_math:
            # 检查是否是块级数学公式的开始
            match = re.match(pattern, line)
            if match:
                text = match.group(1).strip()
                if text and not text.startswith('$$') and not text.startswith('$'):
                    # 这是格式错误：文字后面跟着 $$
                    result.append(text)
                    result.append('')
                    result.append('$$')
                    fixed_count += 1
                    in_math = True
                    continue
            
            # 检查是否是正常的 $$ 开始
            if line.strip() == '$$':
                in_math = True
        else:
            # 在数学公式中
            if line.strip() == '$$':
                in_math = False
        
        result.append(line)
    
    return '\n'.join(result), fixed_count


def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 修复数学公式格式
    content, count1 = fix_display_math_start(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return count1
    
    return 0


def main():
    print("=" * 60)
    print("数学公式格式修复工具")
    print("=" * 60)
    
    total_fixed = 0
    files_fixed = 0
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(root, filename)
            
            # 检查是否包含 $$
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '$$' not in content:
                continue
            
            fixed = process_file(filepath)
            if fixed > 0:
                total_fixed += fixed
                files_fixed += 1
                rel_path = os.path.relpath(filepath, DOCS_DIR)
                print(f"  ✓ {rel_path}: {fixed} 处修复")
    
    print()
    print(f"修复完成!")
    print(f"  修复文件: {files_fixed}")
    print(f"  修复处数: {total_fixed}")


if __name__ == "__main__":
    main()
