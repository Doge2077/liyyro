#!/usr/bin/env python3
"""
MiMo AI 快速修复脚本（分块处理长文件）
"""

import os
import re
import time
import requests
from datetime import datetime

# 配置
DOCS_DIR = "/root/liyyro/docs"
API_KEY = "tp-cmw9lewwxud2vgvk8karmz6vga13b0pqi5t07ldcwtughnmx"
BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1/chat/completions"
MODEL = "mimo-v2.5-pro"
CHUNK_SIZE = 2000  # 每次处理的字符数
REPORT_FILE = "/root/liyyro/scripts/ai-fix-report.md"


def call_mimo(prompt):
    """调用 MiMo API"""
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是 Markdown 修复专家，只返回修复后的内容。"},
            {"role": "user", "content": prompt}
        ],
        "max_completion_tokens": 4096,
        "temperature": 0.2
    }
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            return result.strip() if result else None
    except Exception as e:
        pass
    return None


def process_file(filepath):
    """处理单个文件（分块处理）"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 跳过太短的文件
    if len(content) < 100:
        return "skipped", 0
    
    # 提取 frontmatter
    frontmatter = ""
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = f"---{parts[1]}---"
            body = parts[2]
    
    # 分块处理
    chunks = []
    for i in range(0, len(body), CHUNK_SIZE):
        chunks.append(body[i:i+CHUNK_SIZE])
    
    fixed_chunks = []
    total_fixes = 0
    
    for i, chunk in enumerate(chunks):
        prompt = f"""请修复以下 Markdown 片段中的问题，直接返回修复后的内容，不要添加任何解释。

修复要求：
1. 修复错别字和语法错误
2. 修复 Markdown 格式错误
3. 修复数学公式（$$ 必须独占一行，前面不能有文字）
4. 修复链接格式
5. 不要添加或删除实质性内容

原始内容：
{chunk}"""
        
        result = call_mimo(prompt)
        
        if result and len(result) > len(chunk) * 0.5:
            fixed_chunks.append(result)
            if result != chunk:
                total_fixes += 1
        else:
            fixed_chunks.append(chunk)
        
        time.sleep(0.5)
    
    # 合并结果
    fixed_body = "\n".join(fixed_chunks)
    fixed_content = f"{frontmatter}\n{fixed_body}" if frontmatter else fixed_body
    
    # 保存
    if fixed_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(fixed_content)
        return "fixed", total_fixes
    
    return "no_change", 0


def main():
    print("=" * 60)
    print("MiMo AI 快速修复工具（分块处理）")
    print("=" * 60)
    print(f"模型: {MODEL}")
    print(f"块大小: {CHUNK_SIZE} 字符")
    print()
    
    files = []
    for root, dirs, filenames in os.walk(DOCS_DIR):
        for f in filenames:
            if f.endswith(".md") and f != "index.md":
                files.append(os.path.join(root, f))
    
    files.sort()
    total = len(files)
    fixed = 0
    failed = 0
    skipped = 0
    no_change = 0
    results = []
    
    print(f"共 {total} 个文件\n")
    
    for i, filepath in enumerate(files):
        rel = os.path.relpath(filepath, DOCS_DIR)
        print(f"[{i+1}/{total}] {rel}", end="", flush=True)
        
        try:
            status, fixes = process_file(filepath)
            
            if status == "fixed":
                fixed += 1
                print(f" ✓ ({fixes}块修复)")
            elif status == "skipped":
                skipped += 1
                print(f" -")
            elif status == "no_change":
                no_change += 1
                print(f" =")
            else:
                failed += 1
                print(f" ✗")
            
            results.append({"file": rel, "status": status, "fixes": fixes})
        except Exception as e:
            failed += 1
            print(f" ✗ {e}")
            results.append({"file": rel, "status": "failed", "error": str(e)})
    
    # 生成报告
    report = f"""# MiMo AI 修复报告

**时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**模型**: {MODEL}
**块大小**: {CHUNK_SIZE} 字符

## 统计

| 项目 | 数量 |
|------|------|
| 总文件 | {total} |
| 已修复 | {fixed} |
| 无需修改 | {no_change} |
| 跳过 | {skipped} |
| 失败 | {failed} |

## 详情

"""
    for r in results:
        icon = {"fixed": "✅", "skipped": "-", "no_change": "=", "failed": "❌"}.get(r["status"], "?")
        fixes = f" ({r['fixes']}块)" if r.get("fixes") else ""
        report += f"- {icon} {r['file']}{fixes}\n"
    
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    
    print()
    print("=" * 60)
    print(f"修复完成! 修复:{fixed} 无变化:{no_change} 跳过:{skipped} 失败:{failed}")
    print(f"报告: {REPORT_FILE}")


if __name__ == "__main__":
    main()
