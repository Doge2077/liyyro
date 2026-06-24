---
title: Agent框架选型
---

# Agent框架选型

## 1. 先看控制流

### 1.1 选型前的问题

Agent 框架选型应从控制流开始：任务如何进入，哪些节点由代码控制，哪些节点由模型决策，状态如何持久化，工具如何授权，失败如何恢复。若控制流还没有画清楚，直接比较框架功能容易偏离业务需求。

一个框架适合某类任务，不代表适合所有 Agent。框架越强，抽象越多；抽象能提高开发效率，也会增加排查成本。选型目标是让团队更稳定地交付任务，而非追求组件数量。

### 1.2 对比维度

| 维度 | 关注点 |
| --- | --- |
| 控制流 | 支持工作流、图、循环、handoff 的方式 |
| 状态 | 是否支持持久化、恢复、人机协作 |
| 工具 | schema、权限、错误和结果结构 |
| 观测 | trace、span、评测和回放能力 |
| 部署 | 本地、服务端、队列和并发支持 |
| 生态 | 文档、示例、社区和升级稳定性 |

## 2. 常见框架

### 2.1 框架对比

| 框架 | 适合场景 | 主要关注点 |
| --- | --- | --- |
| OpenAI Agents SDK | 工具、handoff、guardrail、tracing 一体化 | 与 OpenAI 模型和工具生态集成 |
| LangGraph | 图结构、持久状态、人机协作、复杂编排 | 状态机和可恢复执行 |
| CrewAI | 角色分工明确的协作任务 | 内容生产、研究和运营流程 |
| AutoGen AgentChat | 对话式多 Agent 和研究原型 | 多角色对话与实验 |
| 轻量自研 | 控制流简单、需要完全掌控 | 可观测性和治理要自行补齐 |

表格只提供入口。真实项目应以同一批评测任务比较框架，避免只看示例代码是否简短。

### 2.2 迁移成本

迁移成本主要来自状态格式、工具注册方式、trace 数据和错误处理。若工具 schema、状态和评测集保持独立，框架迁移会容易很多。若业务逻辑散落在框架回调中，升级和替换成本会升高。

## 3. 实施建议

### 3.1 小步引入

先用框架实现一个低风险任务，验证工具调用、状态保存、日志、评测和部署。确认这些能力稳定后，再迁移高风险写入任务。不要在第一版同时引入多 Agent、记忆、网关和复杂评估。

### 3.2 框架外资产

以下资产应尽量框架无关：业务用例、工具 schema、评测数据、权限规则、输出格式和错误分类。它们是 Agent 系统的长期资产，框架只是执行载体。

## 参考资料

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Microsoft AutoGen AgentChat](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html)
