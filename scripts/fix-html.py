#!/usr/bin/env python3
"""
修复 Markdown 文件中的 HTML 问题
将未包裹的 XML/HTML 内容包裹在代码块中
"""

import os
import re

DOCS_DIR = "/root/liyyro/docs"

def fix_xml_in_markdown(content):
    """修复未包裹的 XML/HTML 内容"""
    lines = content.split('\n')
    result = []
    in_xml_block = False
    xml_block = []
    
    for line in lines:
        # 检测 XML/HTML 开始标签
        if re.match(r'^\s*<(dependency|groupId|artifactId|version|plugin|configuration|properties|build|project|parent|dependencies|dependencyManagement|repositories|profiles|modules|resources|plugins|exclusions|classifier|scope|optional|type|systemPath|relativePath|modelVersion|packaging|name|description|url|inceptionYear|organization|licenses|developers|contributors|issueManagement|ciManagement|mailingLists|scm|prerequisites|reporting|distributionManagement)', line.strip()):
            if not in_xml_block:
                in_xml_block = True
                xml_block = []
            xml_block.append(line)
            continue
        
        # 检测 XML/HTML 结束标签
        if in_xml_block:
            xml_block.append(line)
            if re.match(r'^\s*</(dependency|groupId|artifactId|version|plugin|configuration|properties|build|project|parent|dependencies|dependencyManagement|repositories|profiles|modules|resources|plugins|exclusions|classifier|scope|optional|type|systemPath|relativePath|modelVersion|packaging|name|description|url|inceptionYear|organization|licenses|developers|contributors|issueManagement|ciManagement|mailingLists|scm|prerequisites|reporting|distributionManagement)', line.strip()):
                # 结束 XML 块
                in_xml_block = False
                # 包裹在代码块中
                result.append('```xml')
                result.extend(xml_block)
                result.append('```')
                xml_block = []
            continue
        
        result.append(line)
    
    return '\n'.join(result)

def main():
    print("修复 Markdown 文件中的 HTML 问题...")
    
    fixed_count = 0
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(root, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含未包裹的 XML
            if '<dependency>' in content or '<groupId>' in content:
                new_content = fix_xml_in_markdown(content)
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    fixed_count += 1
                    print(f"已修复: {os.path.relpath(filepath, DOCS_DIR)}")
    
    print(f"\n修复完成! 共修复 {fixed_count} 个文件")

if __name__ == '__main__':
    main()
