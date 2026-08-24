import streamlit as st
import random
import plotly.graph_objects as go


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="주식 투자 시뮬레이터",
    page_icon="📈",
    layout="centered"
)

st.title("📈 주식 투자 시뮬레이터")
st.caption("축제 주식 동아리 이벤트")


# --------------------------------------------------
# 주식 정보
# --------------------------------------------------

stocks = ["A", "B", "C", "D", "E", "F"]

# 각 회사의 초기 가격 범위
price_ranges = {
    "A": (30000, 45000),
    "B": (35000, 50000),
    "C": (40000, 60000),
    "D": (45000, 65000),
    "E": (50000, 70000),
    "F": (55000, 80000)
}

# 각 회사의 가격 변동성
volatility = {
    "A": 0.04,
    "B": 0.05,
    "C": 0.07,
    "D": 0.08,
    "E": 0.09,
    "F": 0.10
}


# --------------------------------------------------
# 최초 가격 생성
# --------------------------------------------------

if "prices" not in st.session_state:

    st.session_state.prices = {}

    for stock in stocks:

        minimum, maximum = price_ranges[stock]

        st.session_state.prices[stock] = random.randrange(
            minimum,
            maximum + 1,
            5000
        )


# --------------------------------------------------
# 이전 가격 저장
# --------------------------------------------------

if "previous_prices" not in st.session_state:

    st.session_state.previous_prices = {
        stock: st.session_state.prices[stock]
        for stock in stocks
    }


# --------------------------------------------------
# 가격 변동 함수
# --------------------------------------------------

def change_prices():

    for stock in stocks:

        old_price = st.session_state.prices[stock]

        # 종목별 변동성
        max_change = volatility[stock]

        # -변동성 ~ +변동성 사이에서 랜덤 변동
        change_rate = random.uniform(
            -max_change,
            max_change
        )

        new_price = old_price * (1 + change_rate)

        # 너무 급격한 가격 변동 방지
        minimum, maximum = price_ranges[stock]

        minimum_limit = minimum * 0.7
        maximum_limit = maximum * 1.3

        new_price = max(
            minimum_limit,
            min(new_price, maximum_limit)
        )

        # 100원 단위로 정리
        new_price = round(new_price / 100) * 100

        st.session_state.previous_prices[stock] = old_price
        st.session_state.prices[stock] = int(new_price)


# --------------------------------------------------
# 가격 변동 버튼
# --------------------------------------------------

st.subheader("현재 주식 가격")

if st.button(
    "📈 다음 주가 확인",
    use_container_width=True
):
    change_prices()


# --------------------------------------------------
# 현재 가격 및 등락률 계산
# --------------------------------------------------

current_prices = []
change_rates = []

for stock in stocks:

    current_price = st.session_state.prices[stock]
    previous_price = st.session_state.previous_prices[stock]

    if previous_price == 0:
        rate = 0
    else:
        rate = (
            (current_price - previous_price)
            / previous_price
        ) * 100

    current_prices.append(current_price)
    change_rates.append(rate)


# --------------------------------------------------
# 그래프
# --------------------------------------------------

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=stocks,
        y=current_prices,

        text=[
            f"{price:,}원"
            for price in current_prices
        ],

        textposition="outside",

        width=0.55,

        marker=dict(
            cornerradius=10
        )
    )
)

fig.update_layout(

    height=400,

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
            size=16
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
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)


# --------------------------------------------------
# 가격 및 등락률
# --------------------------------------------------

st.subheader("종목별 현재 가격")

cols = st.columns(6)

for i, stock in enumerate(stocks):

    with cols[i]:

        price = current_prices[i]
        rate = change_rates[i]

        if rate > 0:
            rate_text = f"▲ {rate:.2f}%"
        elif rate < 0:
            rate_text = f"▼ {abs(rate):.2f}%"
        else:
            rate_text = "― 0.00%"

        st.markdown(
            f"""
            <div style="
                text-align: center;
                padding: 8px;
            ">
                <div style="
                    font-size: 18px;
                    font-weight: bold;
                ">
                    {stock}
                </div>

                <div style="
                    font-size: 14px;
                    margin-top: 4px;
                ">
                    {price:,}원
                </div>

                <div style="
                    font-size: 13px;
                    margin-top: 3px;
                ">
                    {rate_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
