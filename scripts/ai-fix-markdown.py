#!/usr/bin/env python3
"""
MiMo AI 驱动的 Markdown 批量修复脚本
使用 mimo-v2.5-pro 模型对所有 markdown 文章进行修复和审查
"""

import os
import re
import json
import time
import requests
from datetime import datetime

# 配置
DOCS_DIR = "/root/liyyro/docs"
API_KEY = "tp-cmw9lewwxud2vgvk8karmz6vga13b0pqi5t07ldcwtughnmx"
BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1/chat/completions"
MODEL = "mimo-v2.5-pro"
MAX_RETRIES = 3
MAX_REVIEW_RETRIES = 3
REPORT_FILE = "/root/liyyro/scripts/fix-report.md"

# 修复 Prompt
FIX_PROMPT = """你是一个专业的 Markdown 文档修复专家。请修复以下 Markdown 文章中的问题。

修复要求：
1. 修复错别字和语法错误
2. 修复 Markdown 格式错误（标题层级、列表缩进、代码块标记等）
3. 修复数学公式格式：
   - 块级公式必须独占一行：$$公式内容$$
   - 不能在 $$ 前面有文字（如 "点积定义： $$..." 是错误的）
   - 正确格式：要么 $$ 独占一行，要么使用内联 $...$
   - 确保 LaTeX 语法完整正确
4. 修复代码块（确保代码块完整，语言标记正确）
5. 修复链接格式（确保 [text](url) 格式正确，不能有未闭合的括号）
6. 修复表格格式（确保 Markdown 表格语法正确）
7. 保留原始内容和语义，不要添加或删除实质性内容
8. 保留 frontmatter（--- 之间的内容）不变
9. 图片链接如果已经是 jsDelivr CDN 格式，保持不变

请直接返回修复后的完整 Markdown 内容，不要添加任何解释或代码块标记。

原始内容：
{content}"""

# 审查 Prompt
REVIEW_PROMPT = """你是一个严格的 Markdown 文档审查专家。请审查以下修复后的 Markdown 文章，检查是否还有问题。

审查标准：
1. 是否还有错别字或语法错误
2. Markdown 格式是否正确
3. 数学公式格式是否正确：
   - 块级公式是否独占一行（$$ 前面不能有文字）
   - LaTeX 语法是否完整
4. 代码块是否完整且格式正确
5. 链接格式是否正确
6. 表格格式是否正确

请只回复以下之一：
- "APPROVED" - 如果文档没有问题
- "ISSUES: [具体问题描述]" - 如果还有问题需要修复

修复后的内容：
{content}"""


def call_mimo(prompt, max_tokens=8192):
    """调用 MiMo API"""
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a professional Markdown document repair expert. You should only return the repaired Markdown content without any explanation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_completion_tokens": max_tokens,
        "temperature": 0.3
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(BASE_URL, headers=headers, json=data, timeout=120)
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return content.strip()
            else:
                print(f"    API 错误: {response.status_code} - {response.text[:200]}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(5)
        except Exception as e:
            print(f"    请求异常: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(5)
    
    return None


def fix_markdown(content):
    """修复 Markdown 内容"""
    prompt = FIX_PROMPT.format(content=content)
    return call_mimo(prompt)


def review_markdown(content):
    """审查 Markdown 内容"""
    prompt = REVIEW_PROMPT.format(content=content)
    return call_mimo(prompt, max_tokens=1024)


def process_file(filepath):
    """处理单个文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    # 备份原始内容
    backup_path = filepath + ".bak"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(original_content)
    
    current_content = original_content
    fix_attempts = 0
    review_passed = False
    issues = []
    
    while fix_attempts < MAX_REVIEW_RETRIES and not review_passed:
        fix_attempts += 1
        
        # 修复
        print(f"    修复尝试 {fix_attempts}...")
        fixed_content = fix_markdown(current_content)
        
        if fixed_content is None:
            print(f"    ✗ 修复失败（API 调用失败）")
            issues.append(f"修复尝试 {fix_attempts}: API 调用失败")
            continue
        
        # 检查修复后的内容是否有效
        if len(fixed_content) < len(original_content) * 0.5:
            print(f"    ✗ 修复后内容过短，跳过")
            issues.append(f"修复尝试 {fix_attempts}: 内容过短")
            continue
        
        # 审查
        print(f"    审查中...")
        review_result = review_markdown(fixed_content)
        
        if review_result is None:
            print(f"    ✗ 审查失败（API 调用失败）")
            issues.append(f"审查尝试 {fix_attempts}: API 调用失败")
            current_content = fixed_content
            continue
        
        if "APPROVED" in review_result.upper():
            print(f"    ✓ 审查通过")
            review_passed = True
            current_content = fixed_content
        else:
            print(f"    ✗ 审查未通过: {review_result[:100]}...")
            issues.append(f"审查尝试 {fix_attempts}: {review_result[:200]}")
            current_content = fixed_content
    
    # 保存修复后的内容
    if review_passed and current_content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(current_content)
        
        # 删除备份
        if os.path.exists(backup_path):
            os.remove(backup_path)
        
        return {
            "status": "success",
            "review_passed": True,
            "attempts": fix_attempts,
            "changed": True,
            "issues": issues
        }
    elif current_content != original_content:
        # 保存最后一次修复的内容（即使审查未通过）
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(current_content)
        
        return {
            "status": "partial",
            "review_passed": False,
            "attempts": fix_attempts,
            "changed": True,
            "issues": issues
        }
    else:
        return {
            "status": "no_change",
            "review_passed": False,
            "attempts": fix_attempts,
            "changed": False,
            "issues": issues
        }


def main():
    print("=" * 60)
    print("MiMo AI Markdown 修复工具")
    print("=" * 60)
    print(f"模型: {MODEL}")
    print(f"API: {BASE_URL}")
    print(f"文档目录: {DOCS_DIR}")
    print()
    
    # 收集所有 markdown 文件
    files = []
    for root, dirs, filenames in os.walk(DOCS_DIR):
        for filename in filenames:
            if filename.endswith(".md") and filename != "index.md":
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, DOCS_DIR)
                files.append((rel_path, filepath))
    
    files.sort()
    total_files = len(files)
    
    print(f"找到 {total_files} 个 markdown 文件")
    print()
    
    # 统计
    results = {
        "success": 0,
        "partial": 0,
        "no_change": 0,
        "failed": 0
    }
    all_results = []
    
    # 处理每个文件
    for i, (rel_path, filepath) in enumerate(files):
        print(f"[{i + 1}/{total_files}] 处理: {rel_path}")
        
        try:
            result = process_file(filepath)
            results[result["status"]] += 1
            all_results.append({"file": rel_path, **result})
            
            if result["status"] == "success":
                print(f"  ✓ 修复成功（{result['attempts']} 次尝试）")
            elif result["status"] == "partial":
                print(f"  ⚠ 部分修复（审查未通过）")
            else:
                print(f"  - 无需修改")
        except Exception as e:
            print(f"  ✗ 处理失败: {e}")
            results["failed"] += 1
            all_results.append({"file": rel_path, "status": "failed", "error": str(e)})
        
        # 添加延迟避免 API 限流
        time.sleep(1)
    
    # 生成报告
    report = f"""# MiMo AI Markdown 修复报告

**修复时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**模型**: {MODEL}

## 统计

| 项目 | 数量 |
|------|------|
| 总文件数 | {total_files} |
| 修复成功 | {results['success']} |
| 部分修复 | {results['partial']} |
| 无需修改 | {results['no_change']} |
| 处理失败 | {results['failed']} |

## 详情

"""
    
    for item in all_results:
        status_icon = {"success": "✅", "partial": "⚠️", "no_change": "-", "failed": "❌"}.get(item["status"], "?")
        report += f"### {status_icon} {item['file']}\n\n"
        report += f"- 状态: {item['status']}\n"
        if item.get("attempts"):
            report += f"- 尝试次数: {item['attempts']}\n"
        if item.get("issues"):
            report += f"- 问题:\n"
            for issue in item["issues"]:
                report += f"  - {issue}\n"
        report += "\n"
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    
    print()
    print("=" * 60)
    print("修复完成!")
    print(f"  总文件: {total_files}")
    print(f"  成功: {results['success']}")
    print(f"  部分: {results['partial']}")
    print(f"  无需修改: {results['no_change']}")
    print(f"  失败: {results['failed']}")
    print(f"  报告: {REPORT_FILE}")


if __name__ == "__main__":
    main()
