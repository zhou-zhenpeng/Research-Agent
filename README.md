# Research Agent

基于 **LangGraph + Ollama + Qwen3** 构建的本地智能研究助手，支持联网搜索、工具调用、多步骤 Agent Loop，并通过 Streamlit 提供可视化交互界面。

## 项目亮点

- 基于 LangGraph 构建有状态 Agent 工作流
- 使用 Ollama + Qwen3:4b 本地运行 LLM，无需 LLM API Key
- 支持 Web Search 与 Calculator Tool
- 支持多步骤工具调用与 Agent Loop
- 搜索结果自动展示来源与 URL
- 搜索失败时自动切换搜索后端
- 提供 Streamlit 可视化交互界面

## 系统架构

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
LangGraph Agent
 │
 ▼
Qwen3:4b
 │
 ▼
Conditional Routing
 ├───────────────┐
 ▼               ▼
search_tool   calculator_tool
 └───────┬───────┘
         ▼
      ToolNode
         │
         ▼
      Agent Loop
         │
         ▼
Final Answer + Sources
```

## 多步骤 Tool Calling

例如用户输入：

> 先搜索珠穆朗玛峰的海拔高度，再计算这个数字乘以 2。

Agent 会自动执行：

```text
User Question
     │
     ▼
 search_tool
     │
     ▼
Search Result
     │
     ▼
    Agent
     │
     ▼
calculator_tool
     │
     ▼
Calculation Result
     │
     ▼
Final Answer
```

## 技术栈

| 模块 | 技术 |
|---|---|
| Agent Workflow | LangGraph |
| LLM | Qwen3:4b |
| Local Deployment | Ollama |
| Web Search | DDGS |
| Tool Calling | LangChain Tools |
| Web UI | Streamlit |
| Language | Python |

## 项目结构

```text
Research-Agent/
├── agent.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 快速开始

安装依赖：

```bash
pip install -r requirements.txt
```

下载本地模型：

```bash
ollama pull qwen3:4b
```

启动应用：

```bash
streamlit run app.py
```

如果无法直接使用 `streamlit`：

```bash
python -m streamlit run app.py
```

浏览器访问：

```text
http://localhost:8501
```

## 示例问题

### 联网搜索

```text
搜索一下 LangGraph 是什么，并给出来源
```

### 多工具任务

```text
先搜索珠穆朗玛峰的海拔高度，再计算这个数字乘以 2
```

## 当前能力

```text
LangGraph State        ✅
Agent Node             ✅
Conditional Routing    ✅
ToolNode               ✅
Agent Loop             ✅
Web Search             ✅
Calculator Tool        ✅
Multi-step Tool Calls  ✅
Source Extraction      ✅
Streamlit UI           ✅
```

## Notes

LLM 通过 Ollama 在本地运行，因此不需要配置外部 LLM API Key。

联网搜索依赖外部搜索服务，网络状况可能影响搜索稳定性。