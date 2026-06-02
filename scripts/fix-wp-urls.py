#!/usr/bin/env python3
"""
修复剩余的 WordPress 图片链接
处理缩略图版本（带 -数字x数字 后缀的）
"""

import os
import re

DOCS_DIR = "/root/liyyro/docs"
CDN_PREFIX = "https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images"

def fix_wp_url(match):
    """修复 WordPress URL"""
    full_url = match.group(0)
    # 提取路径部分
    path_match = re.search(r'/uploads/(\d{4})/(\d{2})/(.+?)(?:-\d+x\d+)?(\.\w+)$', full_url)
    if path_match:
        year = path_match.group(1)
        month = path_match.group(2)
        filename = path_match.group(3) + path_match.group(4)
        return f"{CDN_PREFIX}/{year}/{month}/{filename}"
    return full_url

def main():
    print("修复剩余的 WordPress 图片链接...")
    
    total_fixed = 0
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(root, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 匹配所有 WordPress 上传 URL
            new_content = re.sub(
                r'https://lys2021\.com/wp-content/uploads/\d{4}/\d{2}/[^\s\)"\']+',
                fix_wp_url,
                content
            )
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                total_fixed += 1
                print(f"已修复: {os.path.relpath(filepath, DOCS_DIR)}")
    
    print(f"\n修复完成! 共修复 {total_fixed} 个文件")

if __name__ == '__main__':
    main()
