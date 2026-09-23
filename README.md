\# Research Agent



基于 LangGraph + Ollama + Qwen3 构建的本地智能研究助手。



项目支持联网搜索、计算工具调用、多步骤 Agent Loop，并通过 Streamlit 提供可视化交互界面。



\## Features



\- LangGraph 状态管理与 Agent 工作流

\- 本地 Qwen3:4b 模型，无需 LLM API Key

\- Tool Calling

\- Web Search

\- Calculator Tool

\- 多步骤工具调用

\- Agent Loop

\- 搜索来源展示

\- 搜索失败自动切换搜索后端

\- Streamlit Web UI



\## Architecture



```text

User

&#x20;↓

Streamlit

&#x20;↓

LangGraph

&#x20;↓

Agent Node (Qwen3:4b)

&#x20;↓

Conditional Routing

&#x20;├── search\_tool

&#x20;└── calculator\_tool

&#x20;↓

ToolNode

&#x20;↓

Agent Node

&#x20;↓

Final Answer

