import streamlit as st
import random
import plotly.graph_objects as go


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="주식 투자 이벤트",
    page_icon="📈",
    layout="wide"
)


# =========================================================
# ★★★ 여기에서 회사명을 변경하세요 ★★★
# =========================================================

STOCKS = {
    "A": "알파테크",
    "B": "브릿지모터스",
    "C": "크리에이트",
    "D": "디지털랩",
    "E": "이노베이션",
    "F": "퓨처AI"
}


# =========================================================
# 게임 기본 설정
# =========================================================

# 1코인 = 10,000원
COIN_VALUE = 10000

# 참가자 코인 범위
MIN_COINS = 8
MAX_COINS = 12

# 참가자 자산
MIN_MONEY = MIN_COINS * COIN_VALUE
MAX_MONEY = MAX_COINS * COIN_VALUE

# 주가 범위
MARKET_MIN = 20000
MARKET_MAX = 120000

# 모든 주가는 5,000원 단위
PRICE_UNIT = 5000


# =========================================================
# 초기 주가 범위
#
# 8~12만원의 참가자가 플레이하는 것을 고려해서
# 너무 비싼 종목만 몰리지 않도록 구성
# =========================================================

INITIAL_RANGES = {
    "A": (20000, 35000),
    "B": (30000, 45000),
    "C": (35000, 50000),
    "D": (45000, 60000),
    "E": (50000, 70000),
    "F": (60000, 80000)
}


# =========================================================
# 시장 데이터 초기화
# =========================================================

if "market_initialized" not in st.session_state:

    st.session_state.prices = {}

    for stock in STOCKS:

        minimum, maximum = INITIAL_RANGES[stock]

        st.session_state.prices[stock] = random.randrange(
            minimum,
            maximum + PRICE_UNIT,
            PRICE_UNIT
        )

    # 직전 가격
    st.session_state.previous_prices = {
        stock: st.session_state.prices[stock]
        for stock in STOCKS
    }

    # 등락률
    st.session_state.change_rates = {
        stock: 0.0
        for stock in STOCKS
    }

    # 시장 라운드
    st.session_state.round = 0

    st.session_state.market_initialized = True


# =========================================================
# 참가자 데이터 초기화
# =========================================================

if "player_number" not in st.session_state:
    st.session_state.player_number = 1

if "player_coins" not in st.session_state:
    st.session_state.player_coins = MIN_COINS

if "holdings" not in st.session_state:
    st.session_state.holdings = {
        stock: 0
        for stock in STOCKS
    }

if "investment_amount" not in st.session_state:
    st.session_state.investment_amount = 0

if "investment_started" not in st.session_state:
    st.session_state.investment_started = False

if "result_available" not in st.session_state:
    st.session_state.result_available = False


# =========================================================
# 주가 변동 함수
# =========================================================

def change_market():

    for stock in STOCKS:

        old_price = st.session_state.prices[stock]

        chance = random.random()


        # -------------------------------------------------
        # 2% : 초대형 급등 / 급락
        # -------------------------------------------------

        if chance < 0.02:

            change = random.choice([
                30000,
                35000,
                40000
            ])


        # -------------------------------------------------
        # 8% : 급등 / 급락
        # -------------------------------------------------

        elif chance < 0.10:

            change = random.choice([
                20000,
                25000,
                30000
            ])


        # -------------------------------------------------
        # 25% : 큰 변동
        # -------------------------------------------------

        elif chance < 0.35:

            change = random.choice([
                10000,
                15000,
                20000
            ])


        # -------------------------------------------------
        # 65% : 일반 변동
        # -------------------------------------------------

        else:

            change = random.choice([
                5000,
                5000,
                5000,
                10000
            ])


        # 상승 / 하락
        direction = random.choice([-1, 1])

        new_price = old_price + (
            direction * change
        )


        # -------------------------------------------------
        # 가격 제한
        # -------------------------------------------------

        new_price = max(
            MARKET_MIN,
            min(new_price, MARKET_MAX)
        )


        # -------------------------------------------------
        # 5,000원 단위로 정리
        # -------------------------------------------------

        new_price = round(
            new_price / PRICE_UNIT
        ) * PRICE_UNIT


        # -------------------------------------------------
        # 이전 가격 저장
        # -------------------------------------------------

        st.session_state.previous_prices[stock] = old_price


        # -------------------------------------------------
        # 현재 가격 저장
        # -------------------------------------------------

        st.session_state.prices[stock] = int(
            new_price
        )


        # -------------------------------------------------
        # 등락률 계산
        # -------------------------------------------------

        if old_price > 0:

            rate = (
                (new_price - old_price)
                / old_price
            ) * 100

        else:

            rate = 0


        st.session_state.change_rates[stock] = rate


    # 라운드 증가
    st.session_state.round += 1


# =========================================================
# 다음 참가자 초기화
# =========================================================

def reset_player():

    # ★ 시장 가격은 초기화하지 않음

    st.session_state.player_number += 1

    st.session_state.player_coins = MIN_COINS

    st.session_state.holdings = {
        stock: 0
        for stock in STOCKS
    }

    st.session_state.investment_amount = 0

    st.session_state.investment_started = False

    st.session_state.result_available = False


# =========================================================
# 현재 주식 평가금액 계산
# =========================================================

def calculate_stock_value():

    total = 0

    for stock in STOCKS:

        quantity = st.session_state.holdings[stock]

        price = st.session_state.prices[stock]

        total += quantity * price

    return total


# =========================================================
# 주가 변동 결과 팝업
# =========================================================

@st.dialog("📈 주가 변동 결과")
def show_market_result():

    st.subheader(
        f"Round {st.session_state.round}"
    )

    st.write(
        "이번 주식시장의 변동 결과입니다."
    )

    st.divider()


    # =====================================================
    # 회사별 주가 변동
    # =====================================================

    for stock, company in STOCKS.items():

        old_price = (
            st.session_state.previous_prices[stock]
        )

        new_price = (
            st.session_state.prices[stock]
        )

        rate = (
            st.session_state.change_rates[stock]
        )


        col1, col2, col3 = st.columns(
            [1.3, 1.5, 1]
        )


        with col1:

            st.markdown(
                f"### {company}"
            )


        with col2:

            st.write(
                f"{old_price:,}원 → {new_price:,}원"
            )


        with col3:

            if rate > 0:

                st.markdown(
                    f"🔴 **▲ {rate:.2f}%**"
                )

            elif rate < 0:

                st.markdown(
                    f"🔵 **▼ {abs(rate):.2f}%**"
                )

            else:

                st.write(
                    "― 0.00%"
                )


    st.divider()


    # =====================================================
    # 투자 결과
    # =====================================================

    st.subheader("💰 투자 결과")


    # -----------------------------------------------------
    # 현재 보유 주식의 평가금액
    # -----------------------------------------------------

    stock_value = calculate_stock_value()


    # -----------------------------------------------------
    # 참가자가 처음 가지고 있던 총자산
    # -----------------------------------------------------

    total_money = (
        st.session_state.player_coins
        * COIN_VALUE
    )


    # -----------------------------------------------------
    # 투자하지 않고 남겨둔 현금
    # -----------------------------------------------------

    remaining_money = (
        total_money
        - st.session_state.investment_amount
    )


    # -----------------------------------------------------
    # ★ 현재 잔액
    #
    # 주식 평가금액 + 남은 현금
    # -----------------------------------------------------

    current_balance = (
        stock_value
        + remaining_money
    )


    # -----------------------------------------------------
    # 총 수익
    # -----------------------------------------------------

    profit = (
        current_balance
        - total_money
    )


    # -----------------------------------------------------
    # 총 수익률
    # -----------------------------------------------------

    if total_money > 0:

        profit_rate = (
            profit
            / total_money
        ) * 100

    else:

        profit_rate = 0


    # =====================================================
    # 결과 표시
    # =====================================================

    result1, result2 = st.columns(2)


    with result1:

        st.metric(
            "투자금액",
            f"{st.session_state.investment_amount:,}원"
        )


    with result2:

        # ★ 참가자의 실제 최종 잔액
        st.metric(
            "현재 잔액",
            f"{current_balance:,}원"
        )


    result3, result4 = st.columns(2)


    with result3:

        if profit >= 0:

            st.metric(
                "수익",
                f"+{profit:,}원"
            )

        else:

            st.metric(
                "손실",
                f"{profit:,}원"
            )


    with result4:

        st.metric(
            "수익률",
            f"{profit_rate:+.2f}%"
        )


    # =====================================================
    # 수익 / 손실 메시지
    # =====================================================

    if profit > 0:

        st.success(
            f"🎉 **+{profit:,}원 수익!**"
        )

    elif profit < 0:

        st.error(
            f"📉 **{abs(profit):,}원 손실**"
        )

    else:

        st.info(
            "수익도 손실도 없습니다."
        )


    st.divider()


    # =====================================================
    # 다음 참가자
    # =====================================================

    if st.button(
        "👤 다음 참가자",
        use_container_width=True
    ):

        reset_player()

        st.rerun()


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stock-name {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .stock-price {
        font-size: 14px;
        margin-top: -3px;
        margin-bottom: 4px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 제목
# =========================================================

st.title("📈 주식 투자 이벤트")

st.caption(
    f"현재 시장 라운드 : {st.session_state.round}"
)


# =========================================================
# 전체 화면 좌우 분할
# =========================================================

left, right = st.columns(
    [1.35, 1],
    gap="large"
)


# =========================================================
# 왼쪽 : 주식시장
# =========================================================

with left:

    st.subheader("📊 현재 주식시장")


    # =====================================================
    # 현재 가격
    # =====================================================

    current_prices = [
        st.session_state.prices[stock]
        for stock in STOCKS
    ]


    current_rates = [
        st.session_state.change_rates[stock]
        for stock in STOCKS
    ]


    # =====================================================
    # 그래프 색상
    # =====================================================

    bar_colors = []


    for rate in current_rates:

        if rate > 0:

            # 상승 = 빨간색
            bar_colors.append(
                "#E53935"
            )

        elif rate < 0:

            # 하락 = 파란색
            bar_colors.append(
                "#1E88E5"
            )

        else:

            bar_colors.append(
                "#888888"
            )


    # =====================================================
    # 그래프 위 텍스트
    # =====================================================

    graph_text = []


    for price, rate in zip(
        current_prices,
        current_rates
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


    # =====================================================
    # 그래프 생성
    # =====================================================

    fig = go.Figure()


    fig.add_trace(
        go.Bar(

            x=list(STOCKS.values()),

            y=current_prices,

            text=graph_text,

            textposition="outside",

            width=0.55,

            marker=dict(
                color=bar_colors,
                cornerradius=10
            ),

            hovertemplate=
            "<b>%{x}</b><br>"
            "현재가: %{y:,}원"
            "<extra></extra>"
        )
    )


    # =====================================================
    # 그래프 디자인
    # =====================================================

    fig.update_layout(

        height=560,

        margin=dict(
            l=20,
            r=20,
            t=45,
            b=40
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


    # =====================================================
    # 그래프 아래 회사 정보
    # =====================================================

    stock_info = st.columns(6)


    for i, (stock, company) in enumerate(
        STOCKS.items()
    ):

        with stock_info[i]:

            price = (
                st.session_state.prices[stock]
            )

            rate = (
                st.session_state.change_rates[stock]
            )


            st.markdown(
                f"**{company}**"
            )


            st.write(
                f"{price:,}원"
            )


            if rate > 0:

                st.markdown(
                    f"<span style='color:#E53935'>"
                    f"▲ {rate:.2f}%"
                    f"</span>",
                    unsafe_allow_html=True
                )

            elif rate < 0:

                st.markdown(
                    f"<span style='color:#1E88E5'>"
                    f"▼ {abs(rate):.2f}%"
                    f"</span>",
                    unsafe_allow_html=True
                )

            else:

                st.write(
                    "― 0.00%"
                )


# =========================================================
# 오른쪽 : 참가자
# =========================================================

with right:

    st.subheader(
        f"👤 참가자 {st.session_state.player_number}"
    )


    # =====================================================
    # 참가자 자산
    # =====================================================

    asset_col1, asset_col2 = st.columns(2)


    with asset_col1:

        coins = st.number_input(

            "보유 코인",

            min_value=MIN_COINS,

            max_value=MAX_COINS,

            value=MIN_COINS,

            step=1,

            key=f"coins_{st.session_state.player_number}"
        )


    # 총 자산
    total_money = (
        coins * COIN_VALUE
    )


    with asset_col2:

        st.metric(
            "보유 자산",
            f"{total_money:,}원"
        )


    # =====================================================
    # 투자
    # =====================================================

    st.subheader("💵 투자하기")


    buy_quantities = {}


    # =====================================================
    # A / B / C
    # =====================================================

    row1 = st.columns(3)


    for i, (stock, company) in enumerate(
        list(STOCKS.items())[:3]
    ):

        with row1[i]:

            price = (
                st.session_state.prices[stock]
            )


            st.markdown(
                f"<div class='stock-name'>"
                f"{company}"
                f"</div>",
                unsafe_allow_html=True
            )


            st.markdown(
                f"<div class='stock-price'>"
                f"{price:,}원 / 주"
                f"</div>",
                unsafe_allow_html=True
            )


            buy_quantities[stock] = st.number_input(

                "수량",

                min_value=0,

                step=1,

                value=0,

                label_visibility="collapsed",

                key=(
                    f"player_"
                    f"{st.session_state.player_number}_"
                    f"{stock}"
                )
            )


    # =====================================================
    # D / E / F
    # =====================================================

    row2 = st.columns(3)


    for i, (stock, company) in enumerate(
        list(STOCKS.items())[3:]
    ):

        with row2[i]:

            price = (
                st.session_state.prices[stock]
            )


            st.markdown(
                f"<div class='stock-name'>"
                f"{company}"
                f"</div>",
                unsafe_allow_html=True
            )


            st.markdown(
                f"<div class='stock-price'>"
                f"{price:,}원 / 주"
                f"</div>",
                unsafe_allow_html=True
            )


            buy_quantities[stock] = st.number_input(

                "수량",

                min_value=0,

                step=1,

                value=0,

                label_visibility="collapsed",

                key=(
                    f"player_"
                    f"{st.session_state.player_number}_"
                    f"{stock}"
                )
            )


    # =====================================================
    # 투자금액 계산
    # =====================================================

    total_investment = 0


    for stock in STOCKS:

        total_investment += (
            buy_quantities[stock]
            * st.session_state.prices[stock]
        )


    # 남은 돈
    remaining_money = (
        total_money
        - total_investment
    )


    # =====================================================
    # 투자금액 / 남은 금액
    # =====================================================

    money_col1, money_col2 = st.columns(2)


    with money_col1:

        st.metric(
            "투자금액",
            f"{total_investment:,}원"
        )


    with money_col2:

        st.metric(
            "남은 금액",
            f"{remaining_money:,}원"
        )


    # =====================================================
    # 투자 실행
    # =====================================================

    if st.button(
        "💰 투자 실행",
        use_container_width=True
    ):

        # 투자하지 않은 경우
        if total_investment <= 0:

            st.error(
                "최소 한 주 이상 투자해주세요."
            )


        # 보유 자산보다 많이 투자
        elif total_investment > total_money:

            st.error(
                "⚠️ 보유 자산보다 많은 금액을 투자할 수 없습니다."
            )


        # 정상 투자
        else:

            st.session_state.player_coins = coins

            st.session_state.holdings = {
                stock: buy_quantities[stock]
                for stock in STOCKS
            }

            st.session_state.investment_amount = (
                total_investment
            )

            st.session_state.investment_started = True

            st.session_state.result_available = False

            st.success(
                "✅ 투자 완료!"
            )


    # =====================================================
    # 게임 진행
    # =====================================================

    st.divider()

    st.subheader("🎮 게임 진행")


    # =====================================================
    # 주가 변동
    # =====================================================

    if st.button(
        "📈 주가 변동",
        use_container_width=True,
        type="primary"
    ):

        # 투자 전
        if not st.session_state.investment_started:

            st.warning(
                "먼저 투자 실행을 눌러주세요."
            )


        # 투자 완료
        else:

            change_market()

            st.session_state.result_available = True

            show_market_result()
