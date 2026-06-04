#!/usr/bin/env python3
"""
MiMo AI 修复脚本
- 小文件（<4KB）整体传入
- 大文件分块传入
- 超时 5 分钟
- 支持断点续传
"""

import os
import re
import time
import json
import sys
import requests
from datetime import datetime

# 配置
DOCS_DIR = "/root/liyyro/docs"
API_KEY = "tp-cmw9lewwxud2vgvk8karmz6vga13b0pqi5t07ldcwtughnmx"
BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1/chat/completions"
MODEL = "mimo-v2.5-pro"
SMALL_FILE_LIMIT = 4000   # 小于此大小的文件整体传入
CHUNK_SIZE = 2000          # 大文件分块大小
API_TIMEOUT = 300          # 5分钟超时
PROGRESS_FILE = "/root/liyyro/scripts/fix-progress.json"
REPORT_FILE = "/root/liyyro/scripts/fix-report.md"


def log(msg, end="\n"):
    """输出日志并刷新"""
    print(msg, end=end, flush=True)


def call_mimo(chunk):
    """调用 MiMo API"""
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"请修复以下 Markdown 文本中的错别字和格式问题，直接返回修复后的完整文本，不要添加任何解释：\n\n{chunk}"}
        ],
        "max_completion_tokens": 4096,
        "temperature": 0.2
    }
    try:
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=API_TIMEOUT)
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            if result:
                result = result.strip()
                # 移除可能的代码块标记
                if result.startswith("```") and result.endswith("```"):
                    lines = result.split("\n")
                    if len(lines) > 2:
                        result = "\n".join(lines[1:-1])
                if len(result) > 10:
                    return result
    except requests.exceptions.Timeout:
        log("      ⏰ 超时")
    except Exception as e:
        log(f"      ❌ 错误: {str(e)[:80]}")
    return None


def split_into_chunks(text, max_len):
    """将文本按段落拆分成块"""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if current_chunk and len(current_chunk) + len(para) + 2 > max_len:
            chunks.append(current_chunk)
            current_chunk = para
        else:
            current_chunk = current_chunk + "\n\n" + para if current_chunk else para

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
            frontmatter = f"---{parts[1]}---\n\n"
            body = parts[2]

    # 小文件：整体传入
    if len(body) <= SMALL_FILE_LIMIT:
        log(f"    整体修复 ({len(body)} 字符)...", end="")
        result = call_mimo(body)
        if result and len(result) > len(body) * 0.3:
            fixed_content = f"{frontmatter}{result}"
            if fixed_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(fixed_content)
                log(" ✓")
                return "fixed", 1
            log(" =")
            return "no_change", 0
        log(" ✗")
        return "no_change", 0

    # 大文件：分块处理
    chunks = split_into_chunks(body, CHUNK_SIZE)
    log(f"    分块修复 ({len(body)} 字符, {len(chunks)} 块)")

    fixed_chunks = []
    fixed_count = 0

    for i, chunk in enumerate(chunks):
        log(f"      块 {i+1}/{len(chunks)} ({len(chunk)} 字符)...", end="")
        result = call_mimo(chunk)
        if result:
            if result != chunk:
                fixed_count += 1
            fixed_chunks.append(result)
            log(" ✓")
        else:
            fixed_chunks.append(chunk)
            log(" ✗")
        time.sleep(1)

    fixed_body = "\n\n".join(fixed_chunks)
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
    log("=" * 60)
    log("MiMo AI 修复工具")
    log("=" * 60)
    log(f"模型: {MODEL}")
    log(f"小文件阈值: {SMALL_FILE_LIMIT} 字符")
    log(f"大文件块大小: {CHUNK_SIZE} 字符")
    log(f"API 超时: {API_TIMEOUT} 秒")
    log("")

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

    log(f"待处理: {total} 个文件 (已完成: {len(completed)})")
    log("")

    if total == 0:
        log("所有文件已处理完成!")
        return

    for i, (rel, filepath) in enumerate(files):
        log(f"[{i+1}/{total}] {rel}")

        try:
            status, fixes = process_file(filepath)

            if status == "fixed":
                stats["fixed"] += 1
                if fixes > 1:
                    log(f"  ✓ 已修复 ({fixes}块)")
            elif status == "skipped":
                stats["skipped"] += 1
                log(f"  - 跳过")
            else:
                stats["no_change"] += 1

            # 保存进度
            completed.add(rel)
            progress["completed"] = list(completed)
            progress["stats"] = stats
            save_progress(progress)

        except Exception as e:
            log(f"  ✗ 错误: {e}")

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

    log("")
    log("=" * 60)
    log(f"完成! 已修复:{stats['fixed']} 无变化:{stats['no_change']} 跳过:{stats['skipped']}")


if __name__ == "__main__":
    main()
