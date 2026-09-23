import re
import time
from typing import Annotated, TypedDict

from ddgs import DDGS
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


# =========================
# 1. State
# =========================

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# =========================
# 2. Tools
# =========================

@tool
def calculator_tool(a: float, b: float) -> float:
    """计算两个数字的乘积。"""
    return a * b


@tool
def search_tool(query: str) -> str:
    """搜索互联网信息，并返回带来源编号的搜索结果。"""

    backends = [
        "bing",
        "brave",
        "duckduckgo",
        "wikipedia"
    ]

    for backend in backends:
        try:
            print(f"正在尝试搜索引擎：{backend}")

            results = DDGS(
                timeout=15
            ).text(
                query,
                max_results=5,
                backend=backend
            )

            if not results:
                print(f"{backend} 没有返回结果")
                continue

            search_results = []

            for i, item in enumerate(results, start=1):
                title = item.get("title", "")
                body = item.get("body", "")
                href = item.get("href", "")

                search_results.append(
                    f"[S{i}]\n"
                    f"标题：{title}\n"
                    f"摘要：{body}\n"
                    f"链接：{href}"
                )

            if search_results:
                print(f"搜索成功：{backend}")

                return "\n\n".join(search_results)

        except Exception as e:
            print(
                f"{backend} 搜索失败：{e}"
            )

    return "搜索服务暂时不可用，请稍后重试。"
tools = [
    calculator_tool,
    search_tool
]


# =========================
# 3. System Prompt
# =========================

SYSTEM_PROMPT = """
你是一个严谨的 Research Agent。

工作规则：

1. 当问题需要外部事实、最新信息或资料查询时，优先使用 search_tool。
2. 如果使用了 search_tool，最终回答必须主要依据搜索工具返回的内容。
3. 不要把广告、营销口号或夸张描述直接当作客观事实。
4. 引用搜索信息时，在相关内容后标注来源编号，例如 [S1]、[S2]。
5. 如果使用了搜索，最终回答末尾增加“参考来源”。
6. 如果证据不足，要明确说明证据不足，不要自行编造。
7. 数学乘法计算优先使用 calculator_tool。
8. 如果完成任务还需要其他工具，可以继续调用工具，直到任务完成。
9. 回答尽量简洁、清晰、有条理。
"""


# =========================
# 4. Local LLM
# =========================

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)


# =========================
# 5. Agent Node
# =========================

def agent_node(state: AgentState):
    response = llm_with_tools.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *state["messages"]
        ]
    )

    return {
        "messages": [response]
    }


# =========================
# 6. Tool Node
# =========================

tool_node = ToolNode(tools)


# =========================
# 7. LangGraph
# =========================

graph = StateGraph(AgentState)

graph.add_node(
    "agent",
    agent_node
)

graph.add_node(
    "tools",
    tool_node
)

graph.add_edge(
    START,
    "agent"
)

graph.add_conditional_edges(
    "agent",
    tools_condition
)

graph.add_edge(
    "tools",
    "agent"
)

app = graph.compile()


# =========================
# 8. 提取搜索来源
# =========================

def extract_sources(messages):
    sources = []
    seen_urls = set()

    pattern = re.compile(
        r"\[S(\d+)\]\s*\n"
        r"标题：([^\n]+)\n"
        r"摘要：.*?\n"
        r"链接：(https?://[^\s]+)",
        re.S
    )

    for message in messages:
        if getattr(message, "type", "") != "tool":
            continue

        content = str(message.content)

        for match in pattern.finditer(content):
            source_id = match.group(1)
            title = match.group(2).strip()
            url = match.group(3).strip()

            if url in seen_urls:
                continue

            seen_urls.add(url)

            sources.append(
                {
                    "id": f"S{source_id}",
                    "title": title,
                    "url": url
                }
            )

    return sources


# =========================
# 9. 提取 Agent 执行过程
# =========================

def extract_steps(messages):
    steps = []

    for message in messages:
        tool_calls = getattr(message, "tool_calls", None)

        if tool_calls:
            for tool_call in tool_calls:
                name = tool_call.get("name", "unknown_tool")
                args = tool_call.get("args", {})

                steps.append(
                    f"调用工具：{name}，参数：{args}"
                )

    return steps


# =========================
# 10. 对外提供统一调用函数
# =========================

def run_agent(question: str):
    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        }
    )

    messages = result["messages"]

    answer = messages[-1].content
    sources = extract_sources(messages)
    steps = extract_steps(messages)

    return {
        "answer": answer,
        "sources": sources,
        "steps": steps
    }


# =========================
# 11. 命令行测试
# =========================

if __name__ == "__main__":
    question = input("\n请输入你的问题：")

    result = run_agent(question)

    print("\n===== Agent 执行过程 =====")

    for step in result["steps"]:
        print(step)

    print("\n===== 最终回答 =====")
    print(result["answer"])

    if result["sources"]:
        print("\n===== 搜索来源 =====")

        for source in result["sources"]:
            print(
                f"[{source['id']}] "
                f"{source['title']}"
            )
            print(source["url"])
            print()