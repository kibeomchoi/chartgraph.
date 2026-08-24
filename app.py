import streamlit as st
import random
import plotly.graph_objects as go

st.set_page_config(
    page_title="주식 투자 시뮬레이터",
    page_icon="📈",
    layout="centered"
)

st.title("📈 주식 투자 시뮬레이터")

# 주식 종목
stocks = ["A", "B", "C", "D", "E", "F"]

# 최초 주가 생성
if "prices" not in st.session_state:
    st.session_state.prices = {
        stock: random.randrange(50000, 150001, 5000)
        for stock in stocks
    }

# 현재 가격
prices = [
    st.session_state.prices[stock]
    for stock in stocks
]

# 막대그래프
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=stocks,
        y=prices,
        text=[f"{price:,}원" for price in prices],
        textposition="outside",
        width=0.55,
        marker=dict(
            cornerradius=8
        )
    )
)

fig.update_layout(
    height=400,
    width=650,
    margin=dict(
        l=20,
        r=20,
        t=40,
        b=20
    ),
    xaxis=dict(
        title=None,
        tickangle=0,
        tickfont=dict(
            size=15
        ),
        fixedrange=True
    ),
    yaxis=dict(
        title=None,
        tickformat=",",
        fixedrange=True,
        showgrid=True
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=False,
    config={
        "displayModeBar": False
    }
)

# 그래프 아래 가격 표시
cols = st.columns(6)

for i, stock in enumerate(stocks):
    with cols[i]:
        st.markdown(
            f"""
            <div style="
                text-align: center;
                font-size: 14px;
                line-height: 1.5;
            ">
                <b>{stock}</b><br>
                {prices[i]:,}원
            </div>
            """,
            unsafe_allow_html=True
        )
