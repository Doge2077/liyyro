#!/usr/bin/env python3
"""
MiMo AI 修复脚本 v8 - 整篇文章直接修复
不切分，直接传入完整 Markdown
"""

import os
import sys
import time
import json
import html
import requests
from datetime import datetime

# 配置
DOCS_DIR = "/root/liyyro/docs"
API_KEY = "tp-cmw9lewwxud2vgvk8karmz6vga13b0pqi5t07ldcwtughnmx"
BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1/chat/completions"
MODEL = "mimo-v2.5-pro"
API_TIMEOUT = 600  # 10分钟超时
PROGRESS_FILE = "/root/liyyro/scripts/fix-progress.json"
REPORT_FILE = "/root/liyyro/scripts/fix-report.md"
LOG_FILE = "/root/liyyro/scripts/fix.log"


def log(msg, end="\n"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}{end}"
    print(line, end="", flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def call_mimo(content):
    """调用 MiMo API - 传入完整文章"""
    decoded = html.unescape(content)
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"请修复以下 Markdown 文章中的错别字和格式问题，直接返回修复后的完整文章，不要添加任何解释：\n\n{decoded}"}
        ],
        "max_completion_tokens": 16384,
        "temperature": 0.2
    }
    try:
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=API_TIMEOUT)
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            if result and len(result.strip()) > 50:
                return result.strip()
    except requests.exceptions.Timeout:
        log(" ⏰超时")
    except Exception as e:
        log(f" ❌{str(e)[:50]}")
    return None


def process_file(filepath):
    """处理单个文件 - 整篇修复"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if len(content) < 50:
        return "skipped"

    # 提取 frontmatter
    frontmatter = ""
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = f"---{parts[1]}---\n\n"
            body = parts[2]

    log(f" ({len(content)}字符)", end="")

    result = call_mimo(body)

    if result:
        fixed_content = f"{frontmatter}{result}"
        if fixed_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            log(" ✓")
            return "fixed"
        log(" =")
        return "no_change"
    
    log(" ✗")
    return "no_change"


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
    log("MiMo AI 修复工具 v8 (整篇修复)")
    log(f"超时: {API_TIMEOUT}s")
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
            status = process_file(filepath)

            if status == "fixed":
                stats["fixed"] += 1
            elif status == "skipped":
                stats["skipped"] += 1
            else:
                stats["no_change"] += 1

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
