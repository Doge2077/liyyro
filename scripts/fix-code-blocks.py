#!/usr/bin/env python3
"""
修复 Markdown 文件中的缩进代码块
将 4 空格缩进的代码块转换为 ``` 围栏代码块
避免 Vue 模板解析错误
"""

import os
import re

DOCS_DIR = "/root/liyyro/docs"

def fix_indented_code_blocks(content):
    """修复缩进代码块"""
    lines = content.split('\n')
    result = []
    in_code_block = False
    code_block = []
    in_fenced_block = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检测围栏代码块
        if line.strip().startswith('```'):
            in_fenced_block = not in_fenced_block
            result.append(line)
            i += 1
            continue
        
        if in_fenced_block:
            result.append(line)
            i += 1
            continue
        
        # 检测缩进代码块（4空格或1个tab）
        if (line.startswith('    ') or line.startswith('\t')) and line.strip():
            if not in_code_block:
                in_code_block = True
                code_block = []
            
            # 移除缩进
            if line.startswith('    '):
                code_block.append(line[4:])
            else:
                code_block.append(line[1:])
        else:
            if in_code_block:
                # 结束代码块，用 ``` 包裹
                # 检查是否包含 {{ }} 或其他可能被 Vue 解析的内容
                code_content = '\n'.join(code_block)
                if '{{' in code_content or '}}' in code_content or '<' in code_content:
                    result.append('```cpp')
                    result.extend(code_block)
                    result.append('```')
                else:
                    # 如果没有特殊字符，保持原样
                    for cb_line in code_block:
                        result.append('    ' + cb_line)
                
                in_code_block = False
                code_block = []
            
            result.append(line)
        
        i += 1
    
    # 处理文件末尾的代码块
    if in_code_block:
        code_content = '\n'.join(code_block)
        if '{{' in code_content or '}}' in code_content or '<' in code_content:
            result.append('```cpp')
            result.extend(code_block)
            result.append('```')
        else:
            for cb_line in code_block:
                result.append('    ' + cb_line)
    
    return '\n'.join(result)

def main():
    print("修复缩进代码块...")
    
    fixed_count = 0
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(root, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含可能被 Vue 解析的缩进代码块
            if '{{' in content and '    ' in content:
                new_content = fix_indented_code_blocks(content)
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    fixed_count += 1
                    print(f"已修复: {os.path.relpath(filepath, DOCS_DIR)}")
    
    print(f"\n修复完成! 共修复 {fixed_count} 个文件")

if __name__ == '__main__':
    main()
