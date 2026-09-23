import streamlit as st

from agent import run_agent


# =========================
# 页面配置
# =========================

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔎",
    layout="centered"
)


# =========================
# 页面标题
# =========================

st.title("🔎 Research Agent")

st.caption(
    "LangGraph + Qwen3:4b + Ollama + Web Search"
)

st.write(
    "可以进行联网资料搜索、工具调用以及多步骤任务处理。"
)


# =========================
# 用户输入
# =========================

question = st.text_area(
    "请输入你的问题",
    placeholder=(
        "例如：搜索一下 LangGraph 是什么，并给出来源。\n"
        "或者：先搜索珠穆朗玛峰海拔，再计算这个数字乘以 2。"
    ),
    height=120
)


# =========================
# 开始运行
# =========================

if st.button(
    "开始研究",
    type="primary",
    use_container_width=True
):

    if not question.strip():
        st.warning("请先输入一个问题。")

    else:
        try:
            with st.spinner(
                "Agent 正在分析问题并调用工具..."
            ):
                result = run_agent(question)

            # =========================
            # 最终回答
            # =========================

            st.subheader("🤖 Agent 回答")

            st.markdown(
                result["answer"]
            )

            # =========================
            # Agent 执行过程
            # =========================

            if result["steps"]:
                with st.expander(
                    "🧠 查看 Agent 执行过程",
                    expanded=True
                ):
                    for i, step in enumerate(
                        result["steps"],
                        start=1
                    ):
                        st.write(
                            f"步骤 {i}：{step}"
                        )

            # =========================
            # 来源
            # =========================

            if result["sources"]:
                st.subheader("📚 搜索来源")

                for source in result["sources"]:
                    st.markdown(
                        f"**[{source['id']}] "
                        f"{source['title']}**"
                    )

                    st.markdown(
                        f"[打开来源]({source['url']})"
                    )

            else:
                st.caption(
                    "本次任务没有使用联网搜索，"
                    "因此没有搜索来源。"
                )

        except Exception as e:
            st.error(
                f"Agent 运行失败：{e}"
            )