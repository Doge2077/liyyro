# MiMo AI 驱动的 Markdown 批量修复方案

## 一、目标

使用 MiMo-V2.5-Pro 模型对所有 199 篇 Markdown 文章进行自动化修复和审查，并迁移所有非 jsDelivr 图片。

## 二、问题分析

### 2.1 图片现状

| 图片类型 | 数量 | 占比 | 状态 |
|----------|------|------|------|
| jsDelivr CDN | 264 | 66% | ✅ 正常 |
| 非 jsDelivr | 134 | 34% | ❌ 可能无法加载 |

**非 jsDelivr 图片来源**：
- `acwing.com` - 可能有防盗链
- `csdnimg.cn` - 可能有防盗链
- `itbaima.net/cn` - 可能有防盗链
- `arduino.cc` - 链接格式错误（包含 `>`）

### 2.2 需要修复的问题

| 问题类型 | 数量 | 涉及文件数 | 说明 |
|----------|------|------------|------|
| 图片迁移 | 134 | - | 非 jsDelivr 图片需要迁移到 liyyro-photo |
| 数学公式格式 | 329 | 24 | `$$` 前面有文字导致 MathJax 无法识别 |
| 错别字 | 待定 | - | MiMo 修复 |
| 格式错误 | 待定 | - | MiMo 修复 |

**数学公式格式问题详情**：
- **错误格式**：`点积定义： $$\mathbf{a} \cdot \mathbf{b}$$`
- **正确格式**：`$$\mathbf{a} \cdot \mathbf{b}$$`（`$$` 独占一行或内联）
- **受影响文件**：AI（2个）、History/algorithm（9个）、History/cs-fundamentals（6个）、其他（7个）

## 三、MiMo API 配置

| 配置项 | 值 |
|--------|-----|
| API Key | `tp-cmw9lewwxud2vgvk8karmz6vga13b0pqi5t07ldcwtughnmx` |
| Base URL | `https://token-plan-cn.xiaomimimo.com/v1` |
| 模型 | `mimo-v2.5-pro` |
| 协议 | OpenAI 兼容 |

**API 调用格式**：
```python
import requests

response = requests.post(
    "https://token-plan-cn.xiaomimimo.com/v1/chat/completions",
    headers={
        "api-key": "tp-cmw9lewwxud2vgvk8karmz6vga13b0pqi5t07ldcwtughnmx",
        "Content-Type": "application/json"
    },
    json={
        "model": "mimo-v2.5-pro",
        "messages": [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."}
        ],
        "max_completion_tokens": 8192
    }
)
```

## 四、脚本设计

### 4.1 主脚本：`scripts/ai-fix-markdown.py`

**功能流程**：
```
遍历 docs/ 下所有 .md 文件
    ↓
对每个文件：
    1. 读取原始内容
    2. 迁移非 jsDelivr 图片（下载 → 上传到 liyyro-photo → 替换 URL）
    3. 调用 MiMo 进行修复（Fix Pass）
    4. 调用 MiMo 进行审查（Review Pass）
    5. 如果审查不通过，重新修复（最多 3 次）
    6. 保存修复后的文件
    ↓
输出修复报告
```

### 4.2 图片迁移子脚本：`scripts/migrate-external-images.py`

**功能**：
1. 扫描所有 markdown 文件中的图片引用
2. 识别非 jsDelivr CDN 的图片 URL
3. 下载图片到临时目录
4. 上传到 liyyro-photo 仓库（按 年/月 目录结构）
5. 替换 markdown 中的 URL 为 jsDelivr CDN URL
6. 提交 liyyro-photo 仓库

**处理的图片来源**：
- `acwing.com`
- `csdnimg.cn`
- `itbaima.net/cn`
- `arduino.cc`
- 其他外部 URL

**错误处理**：
- 下载失败：记录到错误日志，保留原始 URL
- 图片已存在：跳过上传
- 格式错误的 URL：尝试修复或跳过

### 4.3 修复 Prompt（Fix Pass）

```
你是一个专业的 Markdown 文档修复专家。请修复以下 Markdown 文章中的问题：

修复要求：
1. 修复错别字和语法错误
2. 修复 Markdown 格式错误（标题层级、列表缩进、代码块标记等）
3. 修复数学公式格式：
   - 块级公式必须独占一行：$$公式内容$$
   - 不能在 $$ 前面有文字（如 "点积定义： $$..." 是错误的）
   - 正确格式：要么 $$ 独占一行，要么使用内联 $...$
   - 确保 LaTeX 语法完整正确
4. 修复代码块（确保代码块完整，语言标记正确）
5. 修复链接格式（确保 [text](url) 格式正确）
6. 修复表格格式（确保 Markdown 表格语法正确）
7. 保留原始内容和语义，不要添加或删除实质性内容
8. 保留 frontmatter（--- 之间的内容）不变

请直接返回修复后的完整 Markdown 内容，不要添加任何解释。

原始内容：
{original_content}
```

### 4.4 审查 Prompt（Review Pass）

```
你是一个严格的 Markdown 文档审查专家。请审查以下修复后的 Markdown 文章，检查是否还有问题。

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
{fixed_content}
```

### 4.5 错误处理

- API 调用失败：重试 3 次，每次间隔 5 秒
- 审查不通过：最多重新修复 3 次
- 超过最大重试次数：记录到错误日志，继续处理下一个文件
- 保留原始文件备份（在修改前）

## 五、目录结构

```
scripts/
├── ai-fix-markdown.py           # 主修复脚本
├── migrate-external-images.py   # 外部图片迁移脚本
├── mimo-config.json              # MiMo API 配置
└── fix-report.md                 # 修复报告（运行后生成）
```

## 六、执行步骤

1. **迁移外部图片**：运行 `migrate-external-images.py`
2. **创建修复脚本**：编写 `ai-fix-markdown.py`
3. **测试运行**：先对 1-2 个文件进行测试
4. **全量运行**：对所有 199 个文件执行修复
5. **生成报告**：输出修复统计和详情
6. **提交代码**：将修复后的文件提交到 Git
7. **重新部署**：构建 Docker 镜像并部署

## 七、预期输出

### 7.1 图片迁移输出

```
=== 外部图片迁移工具 ===

扫描到 134 个非 jsDelivr 图片
[1/134] 下载: https://cdn.acwing.com/media/article/image/2024/05/05/xxx.jpg
  ✓ 上传成功 -> https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/05/xxx.jpg

[2/134] 下载: https://img-blog.csdnimg.cn/xxx.png
  ✓ 上传成功 -> https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/06/xxx.png

...

=== 迁移报告 ===
总计图片: 134
成功迁移: 120
下载失败: 10
格式错误: 4

报告已保存到: scripts/image-migration-report.md
```

### 7.2 Markdown 修复输出

```
=== MiMo Markdown 修复工具 ===

[1/199] 修复: AI/大模型基础（一）.md
  ✓ 图片迁移完成 (2 个图片)
  ✓ 修复完成 (修复了 3 个问题)
  ✓ 审查通过

[2/199] 修复: AI/bert模型训练实践.md
  ✓ 修复完成 (修复了 1 个问题)
  ✓ 审查通过

...

=== 修复报告 ===
总计文件: 199
成功修复: 195
审查通过: 190
需要人工审查: 5
失败: 0

报告已保存到: scripts/fix-report.md
```
