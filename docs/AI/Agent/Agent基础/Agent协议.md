---
title: Agent协议
---

# Agent协议

## 1. 按通信边界理解协议

### 1.1 协议解决的问题

一个 Agent 原型可以把模型调用、工具函数、状态和界面写在同一个进程里。系统规模变大后，会出现多个客户端、多个工具服务、多个 Agent 服务和多个模型供应商。若每个边界都使用私有接口，维护成本会迅速上升，权限和审计也很难统一。

Agent 协议的价值在于稳定通信边界。它规定能力如何发现、消息如何表达、任务状态如何流转、错误如何返回、产物如何交付。协议不替 Runtime 做规划，也不替工具实现安全策略；它提供可复用的通信格式，让不同组件能以一致方式协作。

### 1.2 三类通信边界

理解 MCP、A2A、ACP 和 Agent Client Protocol 时，先看通信双方。第一层是客户端到 Agent Runtime，例如 IDE、网页或终端如何提交任务、展示工具事件、确认高风险操作。第二层是 Agent Runtime 到工具和上下文系统，例如文件、数据库、GitHub、浏览器、知识库。第三层是 Agent 到 Agent，例如一个企业助手把子任务委派给另一个专业 Agent。

| 边界 | 典型通信双方 | 代表协议 | 主要问题 |
| --- | --- | --- | --- |
| 客户端到 Agent | IDE、终端、Web UI 与 Agent Runtime | Agent Client Protocol | 会话、事件流、权限确认、文件变更展示 |
| Agent 到工具 | Agent Runtime 与外部数据源或工具服务 | MCP | 工具发现、资源读取、参数 schema、工具结果 |
| Agent 到 Agent | 一个 Agent 与另一个 Agent | A2A、ACP | 能力发现、任务委派、状态跟踪、产物交付 |

下面用编码 Agent 贯穿说明：用户在 IDE 中要求修复一个 bug；编码 Agent 通过客户端协议把进度展示给 IDE；通过 MCP 调用文件搜索、GitHub 和测试工具；需要生成调研摘要时，可以通过 A2A 或 ACP 把子任务交给研究 Agent。

### 1.3 一次完整交互链路

```mermaid
sequenceDiagram
  participant UI as "IDE / 客户端"
  participant Host as "Agent Runtime"
  participant MCP as "MCP Server"
  participant Peer as "专业 Agent"

  UI->>Host: 创建会话并提交修复任务
  Host-->>UI: 返回计划事件与待执行步骤
  Host->>MCP: 初始化连接并获取能力
  MCP-->>Host: 返回 tools、resources、prompts
  Host->>MCP: 调用 search/read/test 等工具
  MCP-->>Host: 返回工具观察结果
  Host->>Peer: 委派调研子任务
  Peer-->>Host: 返回任务状态、摘要和来源
  Host-->>UI: 推送补丁、测试结果和确认请求
  UI->>Host: 用户确认或拒绝高风险操作
  Host-->>UI: 返回最终结果与限制说明
```

这条链路中，每个协议处理不同问题。客户端协议服务用户交互和可视化；MCP 服务工具和上下文接入；A2A/ACP 服务 Agent 间任务协作。分层后，系统更容易替换 UI、替换工具服务或替换下游 Agent。

## 2. MCP 的组成与运行机制

### 2.1 Host、Client、Server

MCP 的全称是 Model Context Protocol。它由 Anthropic 发起，目标是让模型应用以标准方式连接外部上下文和工具。MCP 的基本角色包括 host、client 和 server。

Host 是模型应用或 Agent Runtime，例如 IDE Agent、桌面助手、聊天应用。Client 嵌在 host 内部，负责与某个 MCP server 建立连接、发送协议消息、接收响应。Server 暴露具体能力，例如文件系统、数据库、浏览器、GitHub 或企业 API。

一个 host 可以同时连接多个 server。编码 Agent 可以连接文件系统 server、GitHub server、测试执行 server；企业助手可以连接知识库 server、订单 server、工单 server。模型看到的是 host 汇总后的工具和资源，真实调用通过 client 路由到对应 server。

### 2.2 Data Layer 与 Transport Layer

MCP 可以拆成两层理解。Data layer 定义协议对象和生命周期，例如初始化、能力协商、tools、resources、prompts、sampling、notifications、错误对象。Transport layer 负责消息如何传输，例如本地 stdio、Streamable HTTP。

MCP 使用 JSON-RPC 2.0 表达请求、响应和通知。带 `id` 的消息表示请求，需要对方返回响应；没有 `id` 的消息表示通知，不要求响应。这样既能表达 `tools/call` 这类请求响应，也能表达资源列表变化、进度更新等通知。

常见初始化流程如下：

```mermaid
sequenceDiagram
  participant Host as "Host"
  participant Client as "MCP Client"
  participant Server as "MCP Server"

  Host->>Client: 创建 server 连接
  Client->>Server: initialize
  Server-->>Client: capabilities、protocolVersion、serverInfo
  Client->>Server: initialized notification
  Client->>Server: tools/list、resources/list、prompts/list
  Server-->>Client: 返回可用能力
  Host->>Client: 选择工具并发起调用
  Client->>Server: tools/call
  Server-->>Client: 返回 structured content
  Client-->>Host: 回填观察结果
```

### 2.3 Tools、Resources、Prompts

MCP server 通常暴露三类能力。Tools 表示可执行动作，例如搜索文件、查询数据库、创建工单。Resources 表示可读取上下文，例如文件、文档、记录或查询结果。Prompts 表示可复用提示模板，帮助 host 生成稳定任务输入。

| 能力 | 适合表达 | 编码 Agent 例子 | 主要返回 |
| --- | --- | --- | --- |
| Tool | 有参数、有执行动作、可能失败 | `search_text`、`run_tests`、`create_issue` | 工具结果、错误、元信息 |
| Resource | 可按 URI 读取的上下文 | `file://src/app.ts`、`note://vector-db` | 文本、二进制、元数据 |
| Prompt | 可复用的提示模板 | “基于文件片段解释代码” | 消息模板和变量 |

Tools 适合让模型主动调用，Resources 适合让客户端或模型应用读取上下文，Prompts 适合复用任务结构。三者组合后，一个文件系统 server 可以暴露搜索工具、文件资源和解释代码的 prompt。

### 2.4 Transport：stdio 与 Streamable HTTP

stdio 适合本地工具。Host 启动 server 进程，通过标准输入输出交换 JSON-RPC 消息。它部署简单，适合文件系统、Git、本地 CLI 这类与宿主机器关系紧密的能力。桌面 Agent 和 IDE 插件常用这种方式连接本地 server。

Streamable HTTP 适合远程服务。Server 以 HTTP 服务形式运行，client 通过网络请求建立会话并收发消息。它更适合企业 API、共享知识库、远程浏览器和云端工具。远程传输需要额外考虑认证、租户隔离、限流和网络错误恢复。

选择 transport 时要看部署边界。若能力必须访问本地文件和本地命令，stdio 更直接；若能力需要被多个用户或多个 host 复用，HTTP 更容易运维和扩展。无论选择哪种 transport，工具 schema、权限、结果结构和审计仍由实现方控制。

## 3. 实现一个最小 MCP Server

### 3.1 文件笔记 server 的能力设计

一个最小 MCP server 可以从本地笔记场景开始。它暴露一个搜索 tool、一个按 URI 读取笔记的 resource，以及一个生成整理任务输入的 prompt。这个例子足够小，可以看清 MCP 的组成，又能和《Agent基础概念》中的本地笔记 Agent 对应起来。

| 能力 | 名称 | 作用 |
| --- | --- | --- |
| Tool | `search_notes` | 按关键词搜索内存中的笔记 |
| Resource | `note://{name}` | 读取指定笔记内容 |
| Prompt | `summarize_note` | 生成整理某篇笔记的消息模板 |

真实系统里，server 会访问文件系统或数据库，并做路径、身份和权限检查。下面的教学示例只使用内存字典，重点展示 MCP server 的基本结构。

### 3.2 FastMCP 最小代码

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes")

notes = {
    "vector-db": "向量数据库用于存储 embedding，并支持相似度检索。",
    "rag": "RAG 通常先检索资料，再把片段交给模型生成回答。",
}


@mcp.tool()
def search_notes(keyword: str) -> list[str]:
    # Tool：模型可以主动调用，用于查找候选笔记
    return [name for name, text in notes.items() if keyword in text]


@mcp.resource("note://{name}")
def read_note(name: str) -> str:
    # Resource：host 可以按 URI 读取上下文
    return notes.get(name, "")


@mcp.prompt()
def summarize_note(name: str) -> str:
    # Prompt：复用整理笔记的任务模板
    return f"请整理 note://{name} 的核心概念，并列出依据。"


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

这个 server 启动后，host 可以通过 MCP client 初始化连接，读取它声明的 tools、resources 和 prompts。模型若要查资料，host 可以让它看到 `search_notes` 的工具说明；模型选择工具并生成参数后，host 通过 `tools/call` 把调用发给 server。

### 3.3 Host 侧如何调用

Host 侧并不直接导入上面的函数。它通过 MCP client 与 server 通信，先发现能力，再把模型选择的动作转成协议调用。

```mermaid
sequenceDiagram
  participant Model as "模型"
  participant Host as "Host / Runtime"
  participant Client as "MCP Client"
  participant Server as "notes MCP Server"

  Host->>Client: 连接 stdio server
  Client->>Server: initialize
  Server-->>Client: server capabilities
  Client->>Server: tools/list
  Server-->>Client: search_notes schema
  Host->>Model: 提供 search_notes 工具说明
  Model-->>Host: 请求 search_notes(keyword="向量")
  Host->>Client: tools/call
  Client->>Server: 调用 search_notes
  Server-->>Client: ["vector-db"]
  Client-->>Host: 工具观察结果
  Host->>Model: 回填候选笔记
```

这条链路说明 MCP 的边界：server 暴露能力，client 负责连接和消息，host 决定是否把能力交给模型以及如何处理结果。权限也要分层处理。Server 负责保护自己的数据源；host 负责确认用户是否有权使用某个 server 或某类工具；Runtime 负责把工具调用写入 trace。

### 3.4 最小实现到生产实现

最小 server 只能说明形态，生产实现还需要补齐四类能力。第一，身份认证和授权，尤其是 HTTP transport 和企业数据源。第二，输入校验和输出截断，避免模型生成过宽查询或读取过大资源。第三，错误模型，例如 `NotFound`、`PermissionDenied`、`Timeout`、`RateLimited`。第四，观测能力，包括调用耗时、参数摘要、结果数量、错误和 trace id。

MCP 让工具能力可复用，但可靠性仍来自实现。一个搜索 tool 若没有结果上限，换成 MCP 后仍会污染上下文；一个数据库 tool 若没有权限检查，使用标准协议后仍会泄漏数据。协议提供结构，工程质量来自 server 和 host 的共同约束。

## 4. A2A、ACP 与客户端协议

### 4.1 A2A：Agent 之间的任务委派

A2A 通常指 Agent2Agent Protocol。Google 对 A2A 的介绍强调它用于让不同供应商、不同框架构建的 Agent 彼此协作。A2A 关注的是一个 Agent 如何发现另一个 Agent 的能力、向它发送任务、接收进度、处理长任务状态，并获取最终产物。

在编码 Agent 场景中，A2A 可以用于跨专业协作。主 Agent 负责修改代码，但需要一份“相关框架版本变更说明”。它可以把调研任务委派给 Research Agent。Research Agent 使用自己的搜索工具和资料库，运行一段时间后返回摘要、来源和限制。主 Agent 不需要知道 Research Agent 内部用了哪些工具，只需要理解任务状态和产物格式。

A2A 与 MCP 的差异在调用对象层级。调用 MCP tool 更像调用受控函数，输入参数后得到结果。调用 A2A Agent 更像委派一项任务，对方可能多轮执行、调用自己的工具、维护自己的状态，并持续返回进度。A2A 因此需要更强的任务生命周期表达，例如已接收、运行中、等待输入、失败、取消、完成。

### 4.2 ACP：另一类 Agent 间通信尝试

ACP 常指 Agent Communication Protocol。不同社区和项目对 ACP 的定义略有差异，目标通常是为 Agent 间消息、任务、能力和产物提供通用通信层。它和 A2A 面向的问题相近：多个自治 Agent 如何互相发现、交换任务、传递中间结果、交付最终产物。

ACP 的工程价值在于减少点对点私有集成。若每个 Agent 都只暴露一套自定义 HTTP API，调用方必须单独适配 URL、请求字段、状态查询、错误码和结果格式。ACP 试图把这些共性抽象成协议对象，让 Agent 能声明能力、接收任务、返回状态和发送消息。

使用 ACP 时要注意两点。第一，协议名称相同不代表实现兼容，必须看具体规范版本、SDK 和示例。第二，协议只能标准化通信方式，不能自动统一业务语义。比如“分析客户风险”这个任务，不同组织对风险指标、数据来源、合规要求和输出格式有不同定义。ACP 可以承载请求和产物，业务语义仍要通过 schema、说明文档和评估标准补齐。

### 4.3 Agent Client Protocol 与事件流

Agent Client Protocol 面向客户端和 Agent Runtime 的连接。它常见于 IDE、终端和桌面 Agent 场景。客户端需要的不只是聊天消息，还要展示 Agent 正在读哪些文件、准备运行哪些命令、生成了哪些补丁、测试是否通过、是否需要用户批准。这个协议层把 UI 与 Agent 后端解耦。

客户端协议的核心是事件流。用户提交任务后，Agent Runtime 可能连续发出计划事件、工具开始事件、工具完成事件、权限请求、文件变更、测试结果和最终回答。客户端可以根据事件类型展示不同 UI：工具事件显示进度，权限请求显示确认按钮，文件变更显示 diff，测试结果显示通过或失败。

事件应该包含稳定字段。比如工具开始事件包含 `tool_name`、`arguments_summary`、`risk_level`；工具完成事件包含 `ok`、`summary`、`elapsed_ms`、`truncated`；权限请求包含 `action`、`target`、`reason`、`impact`；文件变更包含 `path`、`diff`、`language`。这些字段让客户端可以做专业展示，也让用户知道 Agent 正在做什么。

### 4.4 长任务、取消与恢复

Agent 任务经常会持续多轮。代码迁移、调研报告、数据清洗和跨系统审批都可能运行较久。协议需要表达任务状态：已接收、运行中、等待用户、等待外部系统、部分完成、失败、取消、完成。A2A/ACP 尤其需要状态机，因为下游 Agent 可能异步执行。Agent Client Protocol 也需要事件流，让客户端能展示实时进度。

长任务还要支持取消和恢复。用户可能改变目标，客户端可能断线，下游工具可能超时。协议如果只定义最终结果，Runtime 很难处理这些情况。更成熟的设计会提供任务 id、事件序列号、检查点、取消请求和错误恢复建议。状态持久化属于实现层，但协议要提供可表达状态的消息结构。

### 4.5 身份、权限与审计

协议互操作不能绕过权限。MCP server 可能连接企业数据库，A2A Agent 可能接收私有文档，客户端协议可能触发本地命令。每一次跨边界调用都要回答四个问题：调用方是谁；它代表哪个用户；本次操作需要什么权限；调用记录如何审计。

身份还要区分用户身份、Agent 身份、工具服务身份和下游 Agent 身份。用户让 Agent 查询数据库时，默认使用 Agent 服务器最高权限会扩大风险；更合理的是基于用户授权、服务策略或二者组合。跨 Agent 委派时，上游 Agent 应只传递必要上下文，并记录委派原因和数据范围。

审计链路应贯穿多个协议。一次最终回答可能经过客户端会话、MCP 工具、A2A 子任务和多次模型调用。日志要能串起 trace id、用户、Agent、工具、参数摘要、结果摘要、授权状态、错误和耗时。没有审计链路，问题发生后很难判断是模型决策、工具实现、协议适配还是下游 Agent 造成的。

## 参考资料

- [Model Context Protocol: Introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Model Context Protocol: Architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- [Model Context Protocol: Server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts)
- [Model Context Protocol: Build a server](https://modelcontextprotocol.io/quickstart/server)
- [MCP Specification](https://modelcontextprotocol.io/specification/)
- [A2A GitHub](https://github.com/a2aproject/A2A)
- [Google Developers Blog: A2A - a new era of agent interoperability](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [Agent Communication Protocol: Introduction](https://agentcommunicationprotocol.dev/introduction/welcome)
- [Agent Client Protocol: Introduction](https://agentclientprotocol.com/get-started/introduction)
- [OpenAI: Practices for governing agentic AI systems](https://openai.com/index/practices-for-governing-agentic-ai-systems/)
- [Microsoft: Agentic AI failure modes and effects analysis](https://www.microsoft.com/en-us/security/security-insider/intelligence-reports/agentic-ai-failure-modes-and-effects-analysis)
