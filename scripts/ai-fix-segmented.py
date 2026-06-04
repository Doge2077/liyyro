#!/usr/bin/env python3
"""
MiMo AI 段落级修复脚本
将 Markdown 按段落拆分，逐段修复，超时自动跳过
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
MAX_CHUNK_LEN = 800  # 每段最大字符数
API_TIMEOUT = 45     # API 超时秒数
REPORT_FILE = "/root/liyyro/scripts/ai-fix-report.md"
PROGRESS_FILE = "/root/liyyro/scripts/ai-fix-progress.json"


def call_mimo(chunk):
    """调用 MiMo API"""
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"请将以下 Markdown 文本重新格式化，使其更加规范。只返回重新格式化后的文本，不要添加任何解释：\n\n{chunk}"}
        ],
        "max_completion_tokens": 2048,
        "temperature": 0.2
    }
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=API_TIMEOUT)
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            if result:
                result = result.strip()
                # 移除可能的代码块标记
                if result.startswith("```"):
                    lines = result.split("\n")
                    if lines[-1].strip() == "```":
                        result = "\n".join(lines[1:-1])
                return result
    except requests.exceptions.Timeout:
        return None
    except Exception as e:
        return None
    return None


def split_into_chunks(text, max_len):
    """将文本按段落拆分成块"""
    # 先按空行拆分成段落
    paragraphs = re.split(r'\n\s*\n', text)
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # 如果当前块加上新段落超过限制，先保存当前块
        if current_chunk and len(current_chunk) + len(para) + 2 > max_len:
            chunks.append(current_chunk)
            current_chunk = para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def process_file(filepath):
    """处理单个文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if len(content) < 50:
        return "skipped", 0, 0
    
    # 提取 frontmatter
    frontmatter = ""
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = f"---{parts[1]}---\n\n"
            body = parts[2]
    
    # 拆分成块
    chunks = split_into_chunks(body, MAX_CHUNK_LEN)
    if not chunks:
        return "skipped", 0, 0
    
    fixed_chunks = []
    fixed_count = 0
    timeout_count = 0
    
    for i, chunk in enumerate(chunks):
        # 跳过太短的块
        if len(chunk) < 30:
            fixed_chunks.append(chunk)
            continue
        
        result = call_mimo(chunk)
        
        if result is None:
            # API 超时或失败，保留原文
            fixed_chunks.append(chunk)
            timeout_count += 1
        elif len(result) < len(chunk) * 0.5:
            # 结果太短，保留原文
            fixed_chunks.append(chunk)
        else:
            if result != chunk:
                fixed_count += 1
            fixed_chunks.append(result)
        
        time.sleep(0.5)
    
    # 合并结果
    fixed_body = "\n\n".join(fixed_chunks)
    fixed_content = f"{frontmatter}{fixed_body}"
    
    # 保存
    if fixed_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(fixed_content)
        return "fixed", fixed_count, timeout_count
    
    return "no_change", 0, timeout_count


def load_progress():
    """加载进度"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"completed": []}


def save_progress(progress):
    """保存进度"""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def main():
    print("=" * 60)
    print("MiMo AI 段落级修复工具")
    print("=" * 60)
    print(f"模型: {MODEL}")
    print(f"块大小: {MAX_CHUNK_LEN} 字符")
    print(f"API 超时: {API_TIMEOUT} 秒")
    print()
    
    # 加载进度
    progress = load_progress()
    completed = set(progress.get("completed", []))
    
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
    fixed = 0
    no_change = 0
    skipped = 0
    results = []
    
    print(f"待处理: {total} 个文件 (已完成: {len(completed)})\n")
    
    for i, (rel, filepath) in enumerate(files):
        print(f"[{i+1}/{total}] {rel}", end="", flush=True)
        
        try:
            status, fixes, timeouts = process_file(filepath)
            
            if status == "fixed":
                fixed += 1
                print(f" ✓ ({fixes}段修复, {timeouts}段超时)")
            elif status == "skipped":
                skipped += 1
                print(f" -")
            else:
                no_change += 1
                if timeouts > 0:
                    print(f" = ({timeouts}段超时)")
                else:
                    print(f" =")
            
            results.append({"file": rel, "status": status, "fixes": fixes, "timeouts": timeouts})
            
            # 保存进度
            completed.add(rel)
            progress["completed"] = list(completed)
            save_progress(progress)
            
        except Exception as e:
            print(f" ✗ {e}")
            results.append({"file": rel, "status": "failed", "error": str(e)})
    
    # 生成报告
    report = f"""# MiMo AI 修复报告

**时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**模型**: {MODEL}
**块大小**: {MAX_CHUNK_LEN} 字符

## 统计

| 项目 | 数量 |
|------|------|
| 本次处理 | {total} |
| 已修复 | {fixed} |
| 无需修改 | {no_change} |
| 跳过 | {skipped} |
| 累计完成 | {len(completed)} |

## 详情

"""
    for r in results:
        icon = {"fixed": "✅", "skipped": "-", "no_change": "=", "failed": "❌"}.get(r["status"], "?")
        extra = ""
        if r.get("fixes"):
            extra += f" ({r['fixes']}段)"
        if r.get("timeouts"):
            extra += f" [{r['timeouts']}段超时]"
        report += f"- {icon} {r['file']}{extra}\n"
    
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    
    print()
    print("=" * 60)
    print(f"本次完成! 修复:{fixed} 无变化:{no_change} 跳过:{skipped}")
    print(f"累计完成: {len(completed)}/199")
    print(f"报告: {REPORT_FILE}")


if __name__ == "__main__":
    main()
