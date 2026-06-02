#!/usr/bin/env python3
"""
URL 替换工具
扫描所有 Markdown 文件，替换图片链接为 jsDelivr CDN URL
"""

import os
import re
import json

DOCS_DIR = "/root/liyyro/docs"
URL_MAPPING_FILE = "/root/liyyro/scripts/url-mapping.json"

def load_url_mapping():
    """加载 URL 映射表"""
    if os.path.exists(URL_MAPPING_FILE):
        with open(URL_MAPPING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def replace_urls_in_file(filepath, url_mapping):
    """替换文件中的 URL"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old_url, new_url in url_mapping.items():
        if old_url in content:
            content = content.replace(old_url, new_url)
            modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("=" * 60)
    print("URL 替换工具")
    print("=" * 60)
    
    # 加载 URL 映射
    url_mapping = load_url_mapping()
    print(f"已加载 {len(url_mapping)} 条 URL 映射")
    
    # 统计
    total_files = 0
    modified_files = 0
    
    # 遍历所有 Markdown 文件
    for root, dirs, files in os.walk(DOCS_DIR):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(root, filename)
            total_files += 1
            
            if replace_urls_in_file(filepath, url_mapping):
                modified_files += 1
                print(f"已更新: {os.path.relpath(filepath, DOCS_DIR)}")
    
    print(f"\n替换完成!")
    print(f"  扫描文件: {total_files}")
    print(f"  更新文件: {modified_files}")

if __name__ == '__main__':
    main()
