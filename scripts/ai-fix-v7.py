#!/usr/bin/env python3
"""
MiMo AI 修复脚本 v7
- 4 并发处理
- systemd 服务运行
- 自动保存进度
"""

import os
import sys
import time
import json
import html
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置
DOCS_DIR = "/root/liyyro/docs"
API_KEY = "tp-cmw9lewwxud2vgvk8karmz6vga13b0pqi5t07ldcwtughnmx"
BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1/chat/completions"
MODEL = "mimo-v2.5-pro"
CHUNK_SIZE = 1500
API_TIMEOUT = 300
MAX_WORKERS = 4  # 4 并发
PROGRESS_FILE = "/root/liyyro/scripts/fix-progress.json"
REPORT_FILE = "/root/liyyro/scripts/fix-report.md"
LOG_FILE = "/root/liyyro/scripts/fix.log"


def log(msg, end="\n"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}{end}"
    print(line, end="", flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def call_mimo(chunk):
    """调用 MiMo API"""
    decoded_chunk = html.unescape(chunk)
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"请修复以下文本中的错别字和格式问题，直接返回修复后的文本：\n\n{decoded_chunk}"}
        ],
        "max_completion_tokens": 4096,
        "temperature": 0.2
    }
    try:
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=API_TIMEOUT)
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            if result and len(result.strip()) > 5:
                return result.strip()
    except:
        pass
    return None


def split_into_chunks(text, max_len):
    """按段落分块"""
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if current and len(current) + len(para) + 2 > max_len:
            chunks.append(current)
            current = para
        else:
            current = current + "\n\n" + para if current else para
    if current:
        chunks.append(current)
    return chunks


def process_chunk(args):
    """处理单个块"""
    i, chunk, total = args
    result = call_mimo(chunk)
    if result:
        return i, result, True
    return i, chunk, False


def process_file(filepath):
    """处理单个文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if len(content) < 50:
        return "skipped", 0

    frontmatter = ""
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = f"---{parts[1]}---\n\n"
            body = parts[2]

    chunks = split_into_chunks(body, CHUNK_SIZE)
    if not chunks:
        return "skipped", 0

    log(f"  {len(body)}字符/{len(chunks)}块")

    fixed_chunks = list(chunks)
    fixed_count = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for i, chunk in enumerate(chunks):
            if len(chunk) < 30:
                continue
            futures.append(executor.submit(process_chunk, (i, chunk, len(chunks))))

        for future in as_completed(futures):
            i, result, success = future.result()
            if success:
                fixed_chunks[i] = result
                fixed_count += 1
                log(f"    [{i+1}/{len(chunks)}] ✓")

    fixed_body = "\n\n".join(fixed_chunks)
    fixed_content = f"{frontmatter}{fixed_body}"

    if fixed_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(fixed_content)
        return "fixed", fixed_count

    return "no_change", 0


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"completed": [], "stats": {"fixed": 0, "no_change": 0, "skipped": 0}}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def main():
    log("=" * 50)
    log("MiMo AI 修复工具 v7 (systemd)")
    log(f"并发: {MAX_WORKERS} | 超时: {API_TIMEOUT}s | 块: {CHUNK_SIZE}")
    log("=" * 50)

    progress = load_progress()
    completed = set(progress.get("completed", []))
    stats = progress.get("stats", {"fixed": 0, "no_change": 0, "skipped": 0})

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
    log(f"待处理: {total} | 已完成: {len(completed)}")
    log("")

    for i, (rel, filepath) in enumerate(files):
        log(f"[{len(completed)+1}/199] {rel}", end="")

        try:
            status, fixes = process_file(filepath)

            if status == "fixed":
                stats["fixed"] += 1
                log(f"  ✓修复{fixes}块")
            elif status == "skipped":
                stats["skipped"] += 1
                log(f"  跳过")
            else:
                stats["no_change"] += 1
                log(f"  无变化")

            completed.add(rel)
            progress["completed"] = list(completed)
            progress["stats"] = stats
            save_progress(progress)

        except Exception as e:
            log(f"  错误: {e}")

    report = f"""# 修复报告

**时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

| 项目 | 数量 |
|------|------|
| 已修复 | {stats['fixed']} |
| 无变化 | {stats['no_change']} |
| 跳过 | {stats['skipped']} |
| 总计 | {len(completed)} |
"""
    with open(REPORT_FILE, "w") as f:
        f.write(report)

    log("")
    log(f"完成! 修复:{stats['fixed']} 无变化:{stats['no_change']} 跳过:{stats['skipped']}")


if __name__ == "__main__":
    main()
