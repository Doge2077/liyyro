#!/usr/bin/env python3
"""
修复常见的 Markdown 格式问题
"""

import os
import re

DOCS_DIR = "/root/liyyro/docs"

def fix_common_issues(content):
    """修复常见格式问题"""
    original = content
    fixes = 0
    
    # 1. 修复连续的 * * * 分隔线（应该用 ---）
    if '* * *' in content:
        content = content.replace('* * *', '---')
        fixes += 1
    
    # 2. 修复 HTML 实体 &amp; 在非 HTML 上下文中
    # 只在 frontmatter 之外处理
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = parts[1]
        body = parts[2]
        # 修复 &amp; 为 &
        if '&amp;' in body:
            body = body.replace('&amp;', '&')
            fixes += 1
        content = f'---{frontmatter}---{body}'
    
    # 3. 修复空的代码块标记
    # 移除孤立的 ``` 行（前后都是空行）
    content = re.sub(r'\n```\n\n```', '\n```', content)
    
    # 4. 修复链接中的 < > 包裹
    # [text](<url>) -> [text](url)
    content = re.sub(r'\[([^\]]+)\]\(<([^>]+)>\)', r'[\1](\2)', content)
    
    if content != original:
        fixes += 1
    
    return content, fixes


def main():
    print("=" * 60)
    print("常见格式修复工具")
    print("=" * 60)
    
    total_fixed = 0
    files_fixed = 0
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(root, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fixed_content, fixes = fix_common_issues(content)
            
            if fixes > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                total_fixed += fixes
                files_fixed += 1
                rel = os.path.relpath(filepath, DOCS_DIR)
                print(f"  ✓ {rel}")
    
    print(f"\n修复完成! 文件:{files_fixed} 处数:{total_fixed}")


if __name__ == "__main__":
    main()
