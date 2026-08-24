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

# 각 회사의 변동 범위
# 숫자가 클수록 한 번에 움직일 수 있는 폭이 커짐
change_ranges = {
    "A": (5000, 5000),
    "B": (5000, 10000),
    "C": (5000, 10000),
    "D": (5000, 10000),
    "E": (5000, 15000),
    "F": (5000, 15000)
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

        minimum, maximum = change_ranges[stock]

        # 상승 또는 하락
        direction = random.choice([-1, 1])

        # 5,000원 단위로 변화
        change = random.randrange(
            minimum,
            maximum + 1,
            5000
        )

        new_price = old_price + (direction * change)

        # 지나치게 낮아지거나 높아지는 것 방지
        minimum_price = price_ranges[stock][0]
        maximum_price = price_ranges[stock][1]

        new_price = max(
            minimum_price,
            min(new_price, maximum_price)
        )

        # 혹시 모를 단위 오류 방지
        new_price = round(new_price / 5000) * 5000

        st.session_state.previous_prices[stock] = old_price
        st.session_state.prices[stock] = int(new_price)


# --------------------------------------------------
# 현재 가격 및 등락률
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
        dtick=10000,
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
# 종목별 가격
# --------------------------------------------------

st.subheader("현재 주가")

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
                padding: 10px 2px;
                border-radius: 10px;
                border: 1px solid rgba(128,128,128,0.25);
            ">
                <div style="
                    font-size: 17px;
                    font-weight: 700;
                ">
                    {stock}
                </div>

                <div style="
                    font-size: 14px;
                    margin-top: 5px;
                ">
                    {price:,}원
                </div>

                <div style="
                    font-size: 13px;
                    margin-top: 4px;
                ">
                    {rate_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# --------------------------------------------------
# 주가 변동 버튼
# --------------------------------------------------

st.write("")

if st.button(
    "📈 주가 변동",
    use_container_width=True
):
    change_prices()
    st.rerun()
