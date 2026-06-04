#!/usr/bin/env python3
"""
MiMo AI 逐段修复脚本（小块处理，后台运行）
"""

import os
import re
import time
import json
import requests
from datetime import datetime

# 配置
DOCS_DIR = "/root/liyyro/docs"
API_KEY = "tp-cmw9lewwxud2vgvk8karmz6vga13b0pqi5t07ldcwtughnmx"
BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1/chat/completions"
MODEL = "mimo-v2.5-pro"
MAX_CHUNK_LEN = 500   # 每段最大字符数
API_TIMEOUT = 30      # API 超时秒数
PROGRESS_FILE = "/root/liyyro/scripts/fix-progress.json"
REPORT_FILE = "/root/liyyro/scripts/fix-report.md"


def call_mimo(chunk):
    """调用 MiMo API"""
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"请将以下 Markdown 文本重新格式化，使其更加规范。只返回重新格式化后的文本，不要添加任何解释：\n\n{chunk}"}
        ],
        "max_completion_tokens": 1024,
        "temperature": 0.2
    }
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=API_TIMEOUT)
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            if result and len(result.strip()) > 10:
                return result.strip()
    except:
        pass
    return None


def split_into_chunks(text, max_len):
    """将文本按段落拆分成块"""
    lines = text.split('\n')
    chunks = []
    current_chunk = ""
    
    for line in lines:
        if current_chunk and len(current_chunk) + len(line) + 1 > max_len:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            if current_chunk:
                current_chunk += '\n' + line
            else:
                current_chunk = line
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def process_file(filepath):
    """处理单个文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if len(content) < 50:
        return "skipped", 0
    
    # 提取 frontmatter
    frontmatter = ""
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = f"---{parts[1]}---\n"
            body = parts[2]
    
    # 拆分成块
    chunks = split_into_chunks(body, MAX_CHUNK_LEN)
    if not chunks:
        return "skipped", 0
    
    fixed_chunks = []
    fixed_count = 0
    
    for chunk in chunks:
        if len(chunk) < 30:
            fixed_chunks.append(chunk)
            continue
        
        result = call_mimo(chunk)
        
        if result and len(result) > len(chunk) * 0.5:
            if result != chunk:
                fixed_count += 1
            fixed_chunks.append(result)
        else:
            fixed_chunks.append(chunk)
        
        time.sleep(0.3)
    
    # 合并结果
    fixed_body = "\n".join(fixed_chunks)
    fixed_content = f"{frontmatter}{fixed_body}"
    
    if fixed_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(fixed_content)
        return "fixed", fixed_count
    
    return "no_change", 0


def load_progress():
    """加载进度"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"completed": [], "stats": {"fixed": 0, "no_change": 0, "skipped": 0}}


def save_progress(progress):
    """保存进度"""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def main():
    print("=" * 60)
    print("MiMo AI 逐段修复工具")
    print("=" * 60)
    print(f"模型: {MODEL}")
    print(f"块大小: {MAX_CHUNK_LEN} 字符")
    print(f"API 超时: {API_TIMEOUT} 秒")
    print()
    
    # 加载进度
    progress = load_progress()
    completed = set(progress.get("completed", []))
    stats = progress.get("stats", {"fixed": 0, "no_change": 0, "skipped": 0})
    
    # 收集文件
    files = []
    for root, dirs, filenames in os.walk(DOCS_DIR):
        for f in filenames:
            if f.endswith(".md") and f != "index.md":
                filepath = os.path.join(root, f)
                rel = os.path.relpath(filepath, DOCS_DIR)
                if rel not in completed:
                    files.append((rel, filepath))
    
    files.sort()
    total = len(files)
    
    print(f"待处理: {total} 个文件 (已完成: {len(completed)})\n")
    
    if total == 0:
        print("所有文件已处理完成!")
        return
    
    for i, (rel, filepath) in enumerate(files):
        print(f"[{i+1}/{total}] {rel}", end="", flush=True)
        
        try:
            status, fixes = process_file(filepath)
            
            if status == "fixed":
                stats["fixed"] += 1
                print(f" ✓ ({fixes}段)")
            elif status == "skipped":
                stats["skipped"] += 1
                print(f" -")
            else:
                stats["no_change"] += 1
                print(f" =")
            
            # 保存进度
            completed.add(rel)
            progress["completed"] = list(completed)
            progress["stats"] = stats
            save_progress(progress)
            
        except Exception as e:
            print(f" ✗ {e}")
    
    # 生成报告
    report = f"""# MiMo AI 修复报告

**时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**模型**: {MODEL}

## 统计

| 项目 | 数量 |
|------|------|
| 已修复 | {stats['fixed']} |
| 无需修改 | {stats['no_change']} |
| 跳过 | {stats['skipped']} |
| 总计 | {len(completed)} |
"""
    
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    
    print()
    print("=" * 60)
    print(f"完成! 已修复:{stats['fixed']} 无变化:{stats['no_change']} 跳过:{stats['skipped']}")


if __name__ == "__main__":
    main()
