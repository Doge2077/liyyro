#!/usr/bin/env python3
"""
WordPress 文章导出工具
从 MySQL 数据库导出文章，转换为 Markdown 格式，替换图片链接
"""

import os
import re
import json
import mysql.connector
import html2text
from datetime import datetime

# 配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'lys2021_com',
    'password': 'FZ4GHdHfFpX384FG',
    'database': 'lys2021_com'
}

DOCS_DIR = "/root/liyyro/docs"
URL_MAPPING_FILE = "/root/liyyro/scripts/url-mapping.json"

# 分类映射：WordPress 分类 -> VitePress 目录
CATEGORY_MAP = {
    'AI': 'AI',
    'Poems': 'Life/poems',
    'Novels': 'Life/novels',
    'ARTICLES': 'Life/articles',
    'Essays': 'Life/essays',
    'University Activities': 'Life/campus',
    'University Homeworks': 'Life/campus',
    'Photos': 'Life/photos',
    'Java': 'History/java',
    'Software Architect': 'History/java',
    'ALGORITHM': 'History/algorithm',
    'Basic Algorithm': 'History/algorithm',
    'Intermediate Algorithm': 'History/algorithm',
    'Q&A': 'History/qa',
    'Linux': 'History/linux',
    'DataBase System': 'History/database',
    'Computer Network': 'History/cs-fundamentals',
    'Principles of Computer Composition': 'History/cs-fundamentals',
    'Compilation Principle': 'History/cs-fundamentals',
    'Data Structure': 'History/cs-fundamentals',
    'Python': 'History/python',
    'Django': 'History/python',
    'C/C++': 'History/cpp',
    'Tips': 'History/tips',
}

def load_url_mapping():
    """加载 URL 映射表"""
    if os.path.exists(URL_MAPPING_FILE):
        with open(URL_MAPPING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def html_to_markdown(html_content, url_mapping):
    """HTML 转 Markdown"""
    converter = html2text.HTML2Text()
    converter.body_width = 0  # 不自动换行
    converter.protect_links = True
    converter.unicode_snob = True
    converter.ignore_images = False
    converter.ignore_links = False
    converter.ignore_emphasis = False
    
    md = converter.handle(html_content)
    
    # 替换图片链接
    for old_url, new_url in url_mapping.items():
        md = md.replace(old_url, new_url)
    
    return md

def sanitize_filename(title):
    """清理文件名"""
    # 移除或替换非法字符
    name = re.sub(r'[<>:"/\\|?*]', '', title)
    name = re.sub(r'\s+', '-', name.strip())
    name = name[:100]  # 限制长度
    return name

def get_category_dir(categories):
    """根据分类确定目录"""
    for cat in categories:
        if cat in CATEGORY_MAP:
            return CATEGORY_MAP[cat]
    return 'History/uncategorized'

def main():
    print("=" * 60)
    print("WordPress 文章导出工具")
    print("=" * 60)
    
    # 加载 URL 映射
    url_mapping = load_url_mapping()
    print(f"已加载 {len(url_mapping)} 条 URL 映射")
    
    # 连接数据库
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor(dictionary=True)
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return
    
    # 查询文章
    query = """
    SELECT p.ID, p.post_title, p.post_date, p.post_content, p.post_name,
           p.post_excerpt, GROUP_CONCAT(t.name) as categories
    FROM wp_posts p
    LEFT JOIN wp_term_relationships tr ON p.ID = tr.object_id
    LEFT JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
    LEFT JOIN wp_terms t ON tt.term_id = t.term_id
    WHERE p.post_type='post' AND p.post_status='publish'
    GROUP BY p.ID
    ORDER BY p.post_date DESC
    """
    
    cursor.execute(query)
    posts = cursor.fetchall()
    
    print(f"找到 {len(posts)} 篇文章")
    
    # 统计
    exported = 0
    errors = []
    
    for post in posts:
        try:
            post_id = post['ID']
            title = post['post_title']
            date = post['post_date']
            content = post['post_content']
            slug = post['post_name']
            excerpt = post['post_excerpt'] or ''
            categories_str = post['categories'] or ''
            
            # 解析分类
            categories = [c.strip() for c in categories_str.split(',') if c.strip()]
            
            # 确定目录
            category_dir = get_category_dir(categories)
            target_dir = os.path.join(DOCS_DIR, category_dir)
            os.makedirs(target_dir, exist_ok=True)
            
            # 生成文件名
            date_str = date.strftime('%Y-%m-%d') if date else '1970-01-01'
            filename = f"{slug}.md"
            filepath = os.path.join(target_dir, filename)
            
            # HTML 转 Markdown
            md_content = html_to_markdown(content, url_mapping)
            
            # 生成 frontmatter
            frontmatter = f"""---
title: "{title}"
date: {date_str}
categories: [{', '.join(categories)}]
description: "{excerpt[:200] if excerpt else ''}"
---

"""
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + md_content)
            
            exported += 1
            if exported % 10 == 0:
                print(f"已导出 {exported} 篇...")
                
        except Exception as e:
            errors.append(f"ID {post.get('ID', '?')}: {str(e)}")
    
    # 关闭连接
    cursor.close()
    db.close()
    
    print(f"\n导出完成!")
    print(f"  成功导出: {exported}")
    print(f"  失败: {len(errors)}")
    
    if errors:
        print("\n失败详情:")
        for err in errors[:10]:
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... 还有 {len(errors) - 10} 个错误")

if __name__ == '__main__':
    main()
