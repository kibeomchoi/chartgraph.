import streamlit as st
import random
import plotly.graph_objects as go


# ==================================================
# 기본 설정
# ==================================================

st.set_page_config(
    page_title="주식 투자 이벤트",
    page_icon="📈",
    layout="wide"
)

st.title("📈 주식 투자 이벤트")
st.caption("주식 동아리 축제 이벤트")


# ==================================================
# 기본 정보
# ==================================================

stocks = ["A", "B", "C", "D", "E", "F"]

initial_ranges = {
    "A": (30000, 45000),
    "B": (35000, 50000),
    "C": (40000, 55000),
    "D": (45000, 60000),
    "E": (50000, 65000),
    "F": (55000, 75000)
}

MARKET_MIN = 10000
MARKET_MAX = 200000


# ==================================================
# 시장 데이터
# ==================================================

if "market_initialized" not in st.session_state:

    st.session_state.prices = {}

    for stock in stocks:

        minimum, maximum = initial_ranges[stock]

        st.session_state.prices[stock] = random.randrange(
            minimum,
            maximum + 1,
            5000
        )

    st.session_state.previous_prices = {
        stock: st.session_state.prices[stock]
        for stock in stocks
    }

    st.session_state.change_rates = {
        stock: 0
        for stock in stocks
    }

    st.session_state.round = 0

    st.session_state.market_initialized = True


# ==================================================
# 참가자 데이터
# ==================================================

if "player_coins" not in st.session_state:
    st.session_state.player_coins = 10

if "holdings" not in st.session_state:
    st.session_state.holdings = {
        stock: 0
        for stock in stocks
    }

if "investment_started" not in st.session_state:
    st.session_state.investment_started = False

if "investment_amount" not in st.session_state:
    st.session_state.investment_amount = 0

if "result_available" not in st.session_state:
    st.session_state.result_available = False


# ==================================================
# 주가 변동
# ==================================================

def change_market():

    for stock in stocks:

        old_price = st.session_state.prices[stock]

        chance = random.random()

        if chance < 0.02:

            change = random.choice([
                30000,
                35000,
                40000,
                45000,
                50000
            ])

        elif chance < 0.10:

            change = random.choice([
                20000,
                25000,
                30000
            ])

        elif chance < 0.35:

            change = random.choice([
                10000,
                15000,
                20000
            ])

        else:

            change = random.choice([
                5000,
                5000,
                5000,
                10000
            ])

        direction = random.choice([-1, 1])

        new_price = old_price + direction * change

        new_price = max(
            MARKET_MIN,
            min(new_price, MARKET_MAX)
        )

        new_price = round(
            new_price / 5000
        ) * 5000

        st.session_state.previous_prices[stock] = old_price

        st.session_state.prices[stock] = int(new_price)

        if old_price != 0:

            rate = (
                (new_price - old_price)
                / old_price
            ) * 100

        else:

            rate = 0

        st.session_state.change_rates[stock] = rate

    st.session_state.round += 1


# ==================================================
# 참가자 초기화
# ==================================================

def reset_player():

    st.session_state.player_coins = 10

    st.session_state.holdings = {
        stock: 0
        for stock in stocks
    }

    st.session_state.investment_started = False

    st.session_state.investment_amount = 0

    st.session_state.result_available = False

    for stock in stocks:

        st.session_state[
            f"buy_{stock}"
        ] = 0


# ==================================================
# 왼쪽 / 오른쪽 화면
# ==================================================

left, right = st.columns(
    [1.25, 1],
    gap="large"
)


# ==================================================
# 왼쪽 - 주식 시장
# ==================================================

with left:

    st.subheader("📈 현재 주식시장")

    current_prices = [
        st.session_state.prices[stock]
        for stock in stocks
    ]

    change_rates = [
        st.session_state.change_rates[stock]
        for stock in stocks
    ]

    bar_colors = []

    for rate in change_rates:

        if rate > 0:
            bar_colors.append("#E53935")

        elif rate < 0:
            bar_colors.append("#1E88E5")

        else:
            bar_colors.append("#777777")


    graph_text = []

    for price, rate in zip(
        current_prices,
        change_rates
    ):

        if rate > 0:

            graph_text.append(
                f"{price:,}원<br>"
                f"▲ {rate:.2f}%"
            )

        elif rate < 0:

            graph_text.append(
                f"{price:,}원<br>"
                f"▼ {abs(rate):.2f}%"
            )

        else:

            graph_text.append(
                f"{price:,}원"
            )


    fig = go.Figure()

    fig.add_trace(
        go.Bar(

            x=stocks,

            y=current_prices,

            text=graph_text,

            textposition="outside",

            width=0.55,

            marker=dict(
                color=bar_colors,
                cornerradius=10
            ),

            hovertemplate=
            "<b>%{x} 주식</b><br>"
            "현재가: %{y:,}원"
            "<extra></extra>"
        )
    )


    fig.update_layout(

        height=560,

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),

        xaxis=dict(
            title=None,
            tickangle=0,
            tickfont=dict(size=16),
            fixedrange=True
        ),

        yaxis=dict(
            title=None,
            tickformat=",",
            dtick=20000,
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


    st.caption(
        f"현재 라운드: {st.session_state.round}"
    )


# ==================================================
# 오른쪽 - 참가자 / 투자
# ==================================================

with right:

    # ----------------------------------------------
    # 참가자 자산
    # ----------------------------------------------

    st.subheader("💰 참가자 자산")

    coins = st.number_input(
        "보유 코인",
        min_value=10,
        max_value=15,
        value=10,
        step=1
    )

    total_money = coins * 10000

    st.info(
        f"보유 자산: **{total_money:,}원**"
    )


    # ----------------------------------------------
    # 투자
    # ----------------------------------------------

    st.subheader("📊 투자할 주식")

    buy_quantities = {}

    for stock in stocks:

        price = st.session_state.prices[stock]

        buy_quantities[stock] = st.number_input(
            f"{stock} ({price:,}원)",
            min_value=0,
            step=1,
            value=0,
            key=f"buy_{stock}"
        )


    total_investment = 0

    for stock in stocks:

        total_investment += (
            buy_quantities[stock]
            * st.session_state.prices[stock]
        )


    remaining_money = (
        total_money
        - total_investment
    )


    st.write(
        f"투자금액: **{total_investment:,}원**"
    )

    st.write(
        f"남은 금액: **{remaining_money:,}원**"
    )


    # ----------------------------------------------
    # 투자 실행
    # ----------------------------------------------

    if st.button(
        "💰 투자 실행",
        use_container_width=True
    ):

        if total_investment <= 0:

            st.error(
                "최소 한 주 이상의 주식을 선택해주세요."
            )

        elif total_investment > total_money:

            st.error(
                "⚠️ 보유 금액보다 투자금액이 많습니다."
            )

        else:

            st.session_state.player_coins = coins

            st.session_state.holdings = {
                stock: buy_quantities[stock]
                for stock in stocks
            }

            st.session_state.investment_amount = (
                total_investment
            )

            st.session_state.investment_started = True

            st.session_state.result_available = False

            st.success(
                "✅ 투자가 완료되었습니다!"
            )


    # ----------------------------------------------
    # 주가 변동
    # ----------------------------------------------

    st.subheader("🎮 게임 진행")

    if st.button(
        "📈 주가 변동",
        use_container_width=True
    ):

        if not st.session_state.investment_started:

            st.warning(
                "먼저 투자를 실행해주세요."
            )

        else:

            change_market()

            st.session_state.result_available = True

            st.rerun()


    # ----------------------------------------------
    # 결과
    # ----------------------------------------------

    if st.session_state.result_available:

        st.subheader("📊 투자 결과")

        final_value = 0

        for stock in stocks:

            quantity = (
                st.session_state.holdings[stock]
            )

            current_price = (
                st.session_state.prices[stock]
            )

            final_value += (
                quantity
                * current_price
            )


        profit = (
            final_value
            - st.session_state.investment_amount
        )


        if st.session_state.investment_amount > 0:

            profit_rate = (
                profit
                / st.session_state.investment_amount
            ) * 100

        else:

            profit_rate = 0


        st.metric(
            "투자금액",
            f"{st.session_state.investment_amount:,}원"
        )

        st.metric(
            "현재 평가금액",
            f"{final_value:,}원",
            f"{profit:+,}원"
        )


        if profit > 0:

            st.success(
                f"🎉 수익: +{profit:,}원 "
                f"(+{profit_rate:.2f}%)"
            )

        elif profit < 0:

            st.error(
                f"📉 손실: {profit:,}원 "
                f"({profit_rate:.2f}%)"
            )

        else:

            st.info(
                "수익도 손실도 없습니다."
            )


        # ------------------------------------------
        # 다음 참가자
        # ------------------------------------------

        if st.button(
            "👤 다음 참가자",
            use_container_width=True
        ):

            reset_player()

            st.rerun()
