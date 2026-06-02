#!/usr/bin/env python3
"""
MiMo AI 快速修复脚本（跳过审查步骤，加快速度）
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
REPORT_FILE = "/root/liyyro/scripts/ai-fix-report.md"

FIX_PROMPT = """请修复以下 Markdown 文章中的问题，直接返回修复后的完整内容，不要添加任何解释。

修复要求：
1. 修复错别字和语法错误
2. 修复 Markdown 格式错误
3. 修复数学公式（$$ 必须独占一行）
4. 修复代码块格式
5. 修复链接格式
6. 修复表格格式
7. 保留 frontmatter 不变
8. 不要添加或删除实质性内容

原始内容：
{content}"""


def call_mimo(prompt):
    """调用 MiMo API"""
    headers = {"api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是 Markdown 修复专家，只返回修复后的内容。"},
            {"role": "user", "content": prompt}
        ],
        "max_completion_tokens": 8192,
        "temperature": 0.2
    }
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=120)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"    API 错误: {e}")
    return None


def process_file(filepath):
    """处理单个文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 跳过太短的文件
    if len(content) < 100:
        return "skipped"
    
    result = call_mimo(FIX_PROMPT.format(content=content))
    
    if result and len(result) > len(content) * 0.5:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result)
        return "fixed"
    return "failed"


def main():
    print("=" * 60)
    print("MiMo AI 快速修复工具")
    print("=" * 60)
    
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
    results = []
    
    print(f"共 {total} 个文件\n")
    
    for i, filepath in enumerate(files):
        rel = os.path.relpath(filepath, DOCS_DIR)
        print(f"[{i+1}/{total}] {rel}")
        
        status = process_file(filepath)
        
        if status == "fixed":
            fixed += 1
            print(f"  ✓ 已修复")
        elif status == "skipped":
            skipped += 1
            print(f"  - 跳过")
        else:
            failed += 1
            print(f"  ✗ 失败")
        
        results.append({"file": rel, "status": status})
        time.sleep(0.5)
    
    # 生成报告
    report = f"""# MiMo AI 修复报告

**时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**模型**: {MODEL}

## 统计

| 项目 | 数量 |
|------|------|
| 总文件 | {total} |
| 已修复 | {fixed} |
| 跳过 | {skipped} |
| 失败 | {failed} |

## 详情

"""
    for r in results:
        icon = {"fixed": "✅", "skipped": "-", "failed": "❌"}[r["status"]]
        report += f"- {icon} {r['file']}\n"
    
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    
    print(f"\n完成! 修复:{fixed} 跳过:{skipped} 失败:{failed}")
    print(f"报告: {REPORT_FILE}")


if __name__ == "__main__":
    main()
