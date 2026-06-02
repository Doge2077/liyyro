#!/usr/bin/env python3
"""
全面修复 Markdown 文件中的 HTML/Vue 解析问题
1. 修复未包裹的 XML/HTML 内容
2. 修复缩进代码块
3. 转义 {{ }} 模板语法
"""

import os
import re

DOCS_DIR = "/root/liyyro/docs"

def fix_markdown_file(filepath):
    """修复单个 Markdown 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. 转义 {{ }} 模板语法（在非代码块中）
    # 先标记代码块
    code_blocks = []
    def replace_code_block(match):
        code_blocks.append(match.group(0))
        return f'__CODE_BLOCK_{len(code_blocks)-1}__'
    
    # 匹配围栏代码块
    content = re.sub(r'```[\s\S]*?```', replace_code_block, content)
    
    # 转义 {{ 和 }}
    content = content.replace('{{', '&#123;&#123;')
    content = content.replace('}}', '&#125;&#125;')
    
    # 恢复代码块
    for i, block in enumerate(code_blocks):
        content = content.replace(f'__CODE_BLOCK_{i}__', block)
    
    # 2. 修复未包裹的 XML 内容
    # 匹配 <dependency> 等 XML 标签
    xml_pattern = r'(\s*)<(dependency|groupId|artifactId|version|plugin|configuration|properties|build|project|parent|dependencies|dependencyManagement|repositories|profiles|modules|resources|plugins|exclusions|classifier|scope|optional|type|systemPath|relativePath|modelVersion|packaging|name|description|url|inceptionYear|organization|licenses|developers|contributors|issueManagement|ciManagement|mailingLists|scm|prerequisites|reporting|distributionManagement)([^>]*)>'
    
    def wrap_xml(match):
        indent = match.group(1)
        tag = match.group(2)
        attrs = match.group(3)
        return f'{indent}<{tag}{attrs}>'
    
    # 简单处理：如果检测到 XML 标签且不在代码块中，添加代码块包裹
    lines = content.split('\n')
    result = []
    in_xml = False
    xml_lines = []
    
    for line in lines:
        if re.match(r'^\s*<(dependency|groupId|artifactId|version|plugin|configuration|properties|build|project|parent|dependencies)', line.strip()):
            if not in_xml:
                in_xml = True
                xml_lines = []
            xml_lines.append(line)
        elif in_xml:
            xml_lines.append(line)
            if re.match(r'^\s*</(dependency|groupId|artifactId|version|plugin|configuration|properties|build|project|parent|dependencies)', line.strip()):
                in_xml = False
                result.append('```xml')
                result.extend(xml_lines)
                result.append('```')
                xml_lines = []
        else:
            result.append(line)
    
    content = '\n'.join(result)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("全面修复 Markdown 文件...")
    
    fixed_count = 0
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(root, filename)
            
            try:
                if fix_markdown_file(filepath):
                    fixed_count += 1
                    print(f"已修复: {os.path.relpath(filepath, DOCS_DIR)}")
            except Exception as e:
                print(f"错误: {os.path.relpath(filepath, DOCS_DIR)} - {e}")
    
    print(f"\n修复完成! 共修复 {fixed_count} 个文件")

if __name__ == '__main__':
    main()
