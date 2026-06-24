---
title: MCP传输机制
---

# MCP传输机制

## 1. 消息层与传输层

### 1.1 分层理解

MCP 的消息语义由 JSON-RPC 表达，传输层负责把这些消息送达。理解这点后，stdio、Streamable HTTP 等方式就容易区分：它们承载同样的协议消息，但适用部署环境不同。

本地工具常用 stdio，远程服务常用 Streamable HTTP。传输选择影响部署、鉴权、负载均衡和故障恢复，但不改变 tools、resources、prompts 的基本语义。

### 1.2 传输对比

| 传输方式 | 适合场景 | 特点 |
| --- | --- | --- |
| stdio | 本地进程、桌面应用、IDE 插件 | 简单、低延迟、随 Host 启动 |
| Streamable HTTP | 远程 Server、云服务、多客户端接入 | 便于鉴权、部署和网络治理 |
| SSE 历史方案 | 早期远程流式通信 | 新实现应按当前规范选择 |

具体支持能力以 MCP 当前规范和 SDK 为准。文档写作时应避免把历史实现当成新项目默认方案。

## 2. stdio

### 2.1 本地进程模型

stdio 模式下，Host 启动一个 Server 子进程，通过标准输入输出交换 JSON-RPC 消息。它适合本地文件、命令行工具、桌面自动化等能力。

```mermaid
flowchart LR
  H["Host"] -->|"stdin JSON-RPC"| S["MCP Server 进程"]
  S -->|"stdout JSON-RPC"| H
  S --> F["本地文件或工具"]
```

stdio 的优势是部署简单，不需要开端口。它的限制也明显：生命周期依赖 Host，跨机器访问和多租户治理需要额外设计。

### 2.2 工程注意点

Server 的 stdout 应只输出协议消息，日志应写 stderr 或专用日志系统。否则 Host 可能把普通日志当成 JSON-RPC 消息解析。长任务应支持进度、取消和超时。

## 3. Streamable HTTP

### 3.1 远程接入

Streamable HTTP 适合把能力做成远程服务。Host 通过 HTTP 与 Server 通信，可以接入网关、鉴权、限流和审计系统。企业知识库、数据库查询和 SaaS API 集成常用这种部署形态。

### 3.2 网络治理

远程 MCP Server 要处理身份、租户、网络边界、请求大小、响应大小和数据脱敏。Host 不应把任意 Server 自动加入高权限工具集合。Server 来源、能力和风险等级都应进入治理流程。

## 参考资料

- [MCP Transports](https://modelcontextprotocol.io/docs/concepts/transports)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
