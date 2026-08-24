import streamlit as st
import random
import plotly.graph_objects as go


# ==================================================
# 기본 설정
# ==================================================

st.set_page_config(
    page_title="주식 투자 시뮬레이터",
    page_icon="📈",
    layout="centered"
)

st.title("📈 주식 투자 시뮬레이터")
st.caption("축제 주식 동아리 이벤트")


# ==================================================
# 주식 정보
# ==================================================

stocks = ["A", "B", "C", "D", "E", "F"]

# 처음 생성될 때의 가격 범위
price_ranges = {
    "A": (30000, 45000),
    "B": (35000, 50000),
    "C": (40000, 60000),
    "D": (45000, 65000),
    "E": (50000, 70000),
    "F": (55000, 80000)
}

# 게임 중 움직일 수 있는 전체 가격 범위
market_min = 20000
market_max = 120000


# ==================================================
# 최초 주가 생성
# ==================================================

if "prices" not in st.session_state:

    st.session_state.prices = {}

    for stock in stocks:

        minimum, maximum = price_ranges[stock]

        st.session_state.prices[stock] = random.randrange(
            minimum,
            maximum + 1,
            5000
        )


# ==================================================
# 이전 가격
# ==================================================

if "previous_prices" not in st.session_state:

    st.session_state.previous_prices = {
        stock: st.session_state.prices[stock]
        for stock in stocks
    }


# ==================================================
# 현재 가격 변동률
# ==================================================

if "change_rates" not in st.session_state:

    st.session_state.change_rates = {
        stock: 0
        for stock in stocks
    }


# ==================================================
# 주가 변동
# ==================================================

def change_prices():

    for stock in stocks:

        old_price = st.session_state.prices[stock]

        # -------------------------------
        # 변동폭 설정
        # -------------------------------

        chance = random.random()

        # 10% 확률로 급격한 변동
        if chance < 0.10:

            change = random.choice([
                15000,
                20000,
                25000,
                30000
            ])

        # 25% 확률로 큰 변동
        elif chance < 0.35:

            change = random.choice([
                10000,
                15000,
                20000
            ])

        # 나머지는 일반적인 변동
        else:

            change = random.choice([
                5000,
                5000,
                5000,
                10000
            ])

        # 상승 / 하락
        direction = random.choice([-1, 1])

        new_price = old_price + direction * change

        # 전체 가격 범위 제한
        new_price = max(
            market_min,
            min(new_price, market_max)
        )

        # 무조건 5,000원 단위
        new_price = round(new_price / 5000) * 5000

        # 이전 가격 저장
        st.session_state.previous_prices[stock] = old_price

        # 새 가격 저장
        st.session_state.prices[stock] = int(new_price)

        # 증감률 계산
        if old_price != 0:

            rate = (
                (new_price - old_price)
                / old_price
            ) * 100

        else:

            rate = 0

        st.session_state.change_rates[stock] = rate


# ==================================================
# 현재 가격
# ==================================================

current_prices = [
    st.session_state.prices[stock]
    for stock in stocks
]

change_rates = [
    st.session_state.change_rates[stock]
    for stock in stocks
]


# ==================================================
# 막대 색상
# ==================================================

bar_colors = []

for rate in change_rates:

    if rate > 0:
        # 상승 = 빨간색
        bar_colors.append("#E53935")

    elif rate < 0:
        # 하락 = 파란색
        bar_colors.append("#1E88E5")

    else:
        # 변동 없음
        bar_colors.append("#777777")


# ==================================================
# 그래프용 증감률 텍스트
# ==================================================

change_text = []

for rate in change_rates:

    if rate > 0:

        change_text.append(
            f"▲ {rate:.2f}%"
        )

    elif rate < 0:

        change_text.append(
            f"▼ {abs(rate):.2f}%"
        )

    else:

        change_text.append(
            "― 0.00%"
        )


# ==================================================
# 그래프
# ==================================================

fig = go.Figure()

fig.add_trace(
    go.Bar(

        x=stocks,

        y=current_prices,

        text=[
            f"{price:,}원<br>{change}"
            for price, change in zip(
                current_prices,
                change_text
            )
        ],

        textposition="outside",

        textfont=dict(
            size=13
        ),

        marker=dict(
            color=bar_colors,
            cornerradius=10
        ),

        width=0.55,

        hovertemplate=
        "<b>%{x} 주식</b><br>" +
        "현재 가격: %{y:,}원" +
        "<extra></extra>"
    )
)


fig.update_layout(

    height=430,

    margin=dict(
        l=20,
        r=20,
        t=55,
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


# ==================================================
# 현재 주가
# ==================================================

st.subheader("현재 주가")

cols = st.columns(6)

for i, stock in enumerate(stocks):

    with cols[i]:

        price = current_prices[i]
        rate = change_rates[i]

        st.markdown(
            f"**{stock}**"
        )

        st.write(
            f"{price:,}원"
        )

        if rate > 0:

            st.markdown(
                f"<span style='color:#E53935; font-weight:bold;'>▲ {rate:.2f}%</span>",
                unsafe_allow_html=True
            )

        elif rate < 0:

            st.markdown(
                f"<span style='color:#1E88E5; font-weight:bold;'>▼ {abs(rate):.2f}%</span>",
                unsafe_allow_html=True
            )

        else:

            st.write(
                "― 0.00%"
            )


# ==================================================
# 주가 변동 버튼
# ==================================================

st.write("")

if st.button(
    "📈 주가 변동",
    use_container_width=True
):

    change_prices()

    st.rerun()
