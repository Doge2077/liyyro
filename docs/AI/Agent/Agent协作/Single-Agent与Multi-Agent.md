---
title: Single-Agent与Multi-Agent
---

# Single-Agent与Multi-Agent

## 1. 从单 Agent 开始

### 1.1 单 Agent 的结构

Single-Agent 用一个 Agent 维护目标、状态和工具集合。它适合任务边界清楚、工具数量有限、权限集中、上下文可控的场景。很多生产系统应先用单 Agent 跑通最小闭环，再评估是否需要拆分。

单 Agent 的优势是简单：状态只有一份，工具调用链路短，调试时容易复现。对代码修复、资料整理、小型企业助手来说，单 Agent 往往足够。

### 1.2 失控信号

| 信号 | 说明 |
| --- | --- |
| 工具列表过长 | 模型频繁选错工具或重复调用 |
| 上下文拥挤 | 多个领域信息混在同一窗口 |
| 权限冲突 | 同一个 Agent 同时拥有只读和高风险写入能力 |
| 任务可并行 | 子任务之间独立，却被单循环串行执行 |
| 专业边界清楚 | 搜索、编码、审查、客服等职责差异明显 |

出现这些信号时，可以考虑多 Agent。拆分前应先尝试阶段化工具、压缩状态和固定外层工作流。若仍然难以控制，再引入多 Agent。

## 2. Multi-Agent 的价值

### 2.1 分工和隔离

Multi-Agent 通过专业分工降低单个 Agent 的负担。Research Agent 只负责资料，Coding Agent 只负责修改，Review Agent 只负责风险审查。每个 Agent 可以有不同工具、指令、模型和预算。

权限隔离是重要收益。只读 Agent 不需要写文件权限，Review Agent 不需要部署权限。高风险动作集中在少数 Agent 中，更容易审计。

### 2.2 成本

多 Agent 会带来通信、状态同步、结果聚合和冲突处理成本。角色越多，越需要清晰的输入输出格式。若只是把一个任务拆成多个会聊天的角色，系统可能变慢且难以调试。

## 3. 选型对比

### 3.1 对比表

| 维度 | Single-Agent | Multi-Agent |
| --- | --- | --- |
| 实现复杂度 | 低 | 高 |
| 状态管理 | 集中 | 需要共享或传递 |
| 调试难度 | 较低 | 需要跨 Agent trace |
| 权限隔离 | 较弱 | 较强 |
| 并行能力 | 有限 | 更适合并行 |
| 适合任务 | 中小型动态任务 | 大型、多专业、长流程任务 |

### 3.2 渐进路径

```mermaid
flowchart LR
  A["固定工作流"] --> B["单 Agent 动态节点"]
  B --> C["阶段化工具和状态"]
  C --> D["按职责拆分 Worker"]
  D --> E["多 Agent 协作和并行"]
```

先让任务可观测，再拆角色。每次拆分都要比较任务成功率、成本、延迟、冲突次数和人工接管率。

## 参考资料

- [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- [Microsoft AutoGen AgentChat](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html)
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
