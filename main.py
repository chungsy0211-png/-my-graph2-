import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# 기본 설정
# ---------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


# ---------------------------------------
# 데이터 불러오기
# ---------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일: 8자리 숫자 → 날짜
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 여러 장르가 "|"로 연결되어 있으면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 숫자형 열 변환
    numeric_columns = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


df = load_data()

st.info(f"총 {len(df)}편의 영화 데이터를 불러왔습니다.")


# =======================================
# 그래프 1. 장르별 영화 편수
# =======================================
st.divider()
st.header("그래프 1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]

fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig1.update_layout(
    legend_title="장르",
    height=550
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_input(
    "장르별 영화 편수에서 알 수 있는 점을 한 문장으로 적어 보세요.",
    placeholder="예: 이 기간에는 ○○ 장르의 영화가 가장 많이 포함되어 있다.",
    key="explanation1"
)


# =======================================
# 그래프 2. 장르별 영화 트리맵
# =======================================
st.divider()
st.header("그래프 2. 장르별 영화 총 관객 트리맵")

# 트리맵용 데이터
treemap_df = df[
    ["genre", "movieNm", "total_audi"]
].copy()

# 결측값 제거
treemap_df = treemap_df.dropna(
    subset=["genre", "movieNm", "total_audi"]
)

# 총 관객이 음수인 데이터가 있다면 제외
treemap_df = treemap_df[treemap_df["total_audi"] >= 0]

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객 트리맵"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=700
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_input(
    "장르별 영화 총 관객 트리맵에서 알 수 있는 점을 한 문장으로 적어 보세요.",
    placeholder="예: 같은 장르 안에서도 영화별 총 관객 수에 큰 차이가 나타난다.",
    key="explanation2"
)


# ---------------------------------------
# 데이터 출처
# ---------------------------------------
st.divider()
st.caption("데이터 출처: KOBIS 영화관입장권통합전산망 데이터")
