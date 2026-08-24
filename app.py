import streamlit as st
import random
import pandas as pd

st.set_page_config(
    page_title="주식 투자 시뮬레이터",
    page_icon="📈",
    layout="wide"
)

st.title("📈 주식 투자 시뮬레이터")
st.write("A~F 6개 회사의 현재 주식 가격")

# 주식 종목
stocks = ["A", "B", "C", "D", "E", "F"]

# 최초 주가 생성
if "prices" not in st.session_state:
    st.session_state.prices = {
        stock: random.randrange(50000, 150001, 5000)
        for stock in stocks
    }

# 현재 가격 표시
st.subheader("현재 주식 가격")

cols = st.columns(6)

for i, stock in enumerate(stocks):
    with cols[i]:
        st.metric(
            label=f"{stock} 주식",
            value=f"{st.session_state.prices[stock]:,}원"
        )

# 막대그래프용 데이터
chart_data = pd.DataFrame({
    "주식": stocks,
    "가격": [st.session_state.prices[stock] for stock in stocks]
})

# 막대그래프
st.subheader("📊 주식 가격 비교")

st.bar_chart(
    chart_data,
    x="주식",
    y="가격",
    height=400
)
