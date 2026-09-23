\# Research Agent

基于 LangGraph + Ollama + Qwen3 构建的本地智能研究助手。

项目支持联网搜索、计算工具调用、多步骤 Agent Loop，并通过 Streamlit 提供可视化交互界面。
Research Agent
↓
网页效果图
↓
Features
↓
Architecture
↓
运行方法

User
  ↓
Streamlit UI
  ↓
LangGraph Agent
  ↓
Qwen3:4b
  ↓
Conditional Routing
 ┌───────────────┐
 │               │
search_tool   calculator_tool
 │               │
 └────→ ToolNode ←┘
          ↓
       Agent Loop
          ↓
   Final Answer + Sources
