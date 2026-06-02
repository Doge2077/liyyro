#!/usr/bin/env python3
"""
WordPress 图片迁移到 liyyro-photo 仓库
扫描 WordPress 上传目录，过滤缩略图，复制到图床仓库，生成 URL 映射表
"""

import os
import re
import json
import shutil
import hashlib
from datetime import datetime

# 配置
WP_UPLOADS = "/var/www/html/wp-content/uploads"
BLOG_ASSETS = "/root/liyyro-photo/images"
URL_MAPPING_FILE = "/root/liyyro/scripts/url-mapping.json"

# jsDelivr CDN 前缀
CDN_PREFIX = "https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images"

def is_thumbnail(filename):
    """判断是否为 WordPress 缩略图（文件名含 -数字x数字 后缀）"""
    return bool(re.search(r'-\d+x\d+\.\w+$', filename))

def get_original_filename(filename):
    """获取原始文件名（去除缩略图后缀）"""
    return re.sub(r'-\d+x\d+(\.\w+)$', r'\1', filename)

def calculate_hash(filepath):
    """计算文件 MD5 哈希（前8位）"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

def main():
    print("=" * 60)
    print("WordPress 图片迁移工具")
    print("=" * 60)
    
    # 检查目录
    if not os.path.exists(WP_UPLOADS):
        print(f"错误: WordPress 上传目录不存在: {WP_UPLOADS}")
        return
    
    # 创建目标目录
    os.makedirs(BLOG_ASSETS, exist_ok=True)
    
    # URL 映射表
    url_mapping = {}
    
    # 统计
    total_files = 0
    copied_files = 0
    skipped_thumbnails = 0
    
    # 遍历年/月目录
    for year_dir in sorted(os.listdir(WP_UPLOADS)):
        year_path = os.path.join(WP_UPLOADS, year_dir)
        if not os.path.isdir(year_path) or not year_dir.isdigit():
            continue
            
        for month_dir in sorted(os.listdir(year_path)):
            month_path = os.path.join(year_path, month_dir)
            if not os.path.isdir(month_path):
                continue
            
            # 创建目标目录
            target_dir = os.path.join(BLOG_ASSETS, year_dir, month_dir)
            os.makedirs(target_dir, exist_ok=True)
            
            for filename in sorted(os.listdir(month_path)):
                total_files += 1
                src = os.path.join(month_path, filename)
                
                if not os.path.isfile(src):
                    continue
                
                # 跳过缩略图
                if is_thumbnail(filename):
                    skipped_thumbnails += 1
                    continue
                
                # 复制文件
                dst = os.path.join(target_dir, filename)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    copied_files += 1
                
                # 记录 URL 映射
                old_url = f"https://lys2021.com/wp-content/uploads/{year_dir}/{month_dir}/{filename}"
                new_url = f"{CDN_PREFIX}/{year_dir}/{month_dir}/{filename}"
                url_mapping[old_url] = new_url
    
    # 保存 URL 映射表
    os.makedirs(os.path.dirname(URL_MAPPING_FILE), exist_ok=True)
    with open(URL_MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(url_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\n迁移完成!")
    print(f"  总文件数: {total_files}")
    print(f"  跳过缩略图: {skipped_thumbnails}")
    print(f"  复制文件数: {copied_files}")
    print(f"  URL 映射数: {len(url_mapping)}")
    print(f"  映射表已保存到: {URL_MAPPING_FILE}")
    print(f"  图床仓库路径: {BLOG_ASSETS}")

if __name__ == '__main__':
    main()
