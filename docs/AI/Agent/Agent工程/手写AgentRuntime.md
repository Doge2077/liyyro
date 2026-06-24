---
title: 手写AgentRuntime
---

# 手写AgentRuntime

## 1. Runtime 的职责

### 1.1 最小边界

Agent Runtime 是模型和外部系统之间的执行层。它负责组装上下文、调用模型、解析动作、校验工具参数、执行工具、更新状态、判断终止。模型负责提出候选动作，Runtime 负责让动作在安全边界内落地。

手写 Runtime 的价值在于理解底层机制。框架可以提高效率，但核心问题仍然存在：工具如何注册，状态如何保存，错误如何反馈，何时停止，哪些动作需要确认。

### 1.2 核心模块

| 模块 | 职责 |
| --- | --- |
| Model Adapter | 统一模型调用和工具调用格式 |
| Tool Registry | 注册工具 schema、权限和执行函数 |
| State Store | 保存任务目标、轨迹、证据、预算 |
| Policy Engine | 校验权限、路径、风险和确认状态 |
| Runner | 驱动循环、处理错误、判断终止 |
| Trace Logger | 记录模型、工具、状态和结果 |

## 2. 最小代码骨架

### 2.1 Python 示例

```python
class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, schema, func, risk="read"):
        self.tools[name] = {"schema": schema, "func": func, "risk": risk}

    def call(self, name, args):
        tool = self.tools[name]
        # 真实系统应在这里做 JSON schema 和权限校验
        return tool["func"](**args)


def run_agent(goal, model, registry, max_steps=6):
    state = {"goal": goal, "trace": [], "step": 0}

    while state["step"] < max_steps:
        action = model.decide(state, registry.tools)

        if action["type"] == "final":
            return {"answer": action["content"], "trace": state["trace"]}

        result = registry.call(action["tool"], action["args"])
        state["trace"].append({"action": action, "result": result})
        state["step"] += 1

    return {"answer": "达到最大轮次，任务停止。", "trace": state["trace"]}
```

这段骨架省略了生产细节，但展示了最小闭环。后续可以逐步加入 schema 校验、路径限制、超时、审计、人工确认和状态持久化。

### 2.2 终止条件

Runtime 不能只等待模型说完成。常见终止条件包括：达到最大轮次、成本超限、连续无新增证据、工具返回不可恢复错误、用户拒绝高风险动作、评估器通过、任务产物生成成功。

## 3. 框架迁移准备

### 3.1 保持框架无关

手写 Runtime 时，应把工具 schema、状态结构、评测数据和权限策略设计成框架无关。未来迁移到 OpenAI Agents SDK、LangGraph 或 AutoGen 时，这些核心资产可以复用。

### 3.2 何时引入框架

当系统需要图结构状态、多人协作、持久化、handoff、复杂 tracing 或大量工具治理时，引入框架能减少重复开发。若只是只读搜索和简单工具调用，轻量 Runtime 更容易调试。

## 参考资料

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
