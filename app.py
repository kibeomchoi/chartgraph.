import streamlit as st
import random

st.set_page_config(
    page_title="주식 투자 시뮬레이터",
    page_icon="📈",
    layout="wide"
)

st.title("📈 주식 투자 시뮬레이터")
st.write("A~F 6개 회사의 주식 가격을 확인해보세요.")

# 주식 종목
stocks = ["A", "B", "C", "D", "E", "F"]

# 최초 주가 생성
if "prices" not in st.session_state:
    st.session_state.prices = {
        stock: random.randrange(50000, 150001, 5000)
        for stock in stocks
    }

st.subheader("현재 주식 가격")

cols = st.columns(6)

for i, stock in enumerate(stocks):
    with cols[i]:
        st.metric(
            label=f"{stock} 주식",
            value=f"{st.session_state.prices[stock]:,}원"
        )
