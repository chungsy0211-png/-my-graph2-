import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 페이지 설정
# ==========================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# ==========================================
# 데이터 불러오기
# ==========================================
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 숫자형 데이터 변환
    number_columns = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10"
    ]

    for col in number_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # 장르 처리
    if "genre" in df.columns:
        df["genre"] = (
            df["genre"]
            .fillna("미상")
            .astype(str)
            .str.split("|")
            .str[0]
            .str.strip()
        )

    # 제작 국가 처리
    if "nation" in df.columns:
        df["nation"] = (
            df["nation"]
            .fillna("미상")
            .astype(str)
            .str.strip()
        )

    # 개봉일 변환
    if "openDt" in df.columns:
        df["openDt"] = pd.to_datetime(
            df["openDt"].astype(str),
            format="%Y%m%d",
            errors="coerce"
        )

    return df


df = load_data()

st.info(f"총 {len(df)}편의 영화 데이터를 불러왔습니다.")


# ==========================================
# 그래프 1
# 장르별 영화 편수
# ==========================================
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
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig1.update_layout(
    height=550,
    legend_title="장르"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "그래프 1에서 알 수 있는 점을 한 문장으로 적어 보세요.",
    key="explanation1",
    placeholder="예: 이 기간에는 ○○ 장르의 영화가 가장 많다."
)


# ==========================================
# 그래프 2
# 장르별 총 관객 트리맵
# ==========================================
st.divider()
st.header("그래프 2. 장르별 영화 총 관객 트리맵")

treemap_df = df[
    ["genre", "movieNm", "total_audi"]
].copy()

treemap_df = treemap_df.dropna(
    subset=["genre", "movieNm", "total_audi"]
)

treemap_df = treemap_df[
    treemap_df["total_audi"] >= 0
]

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

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "그래프 2에서 알 수 있는 점을 한 문장으로 적어 보세요.",
    key="explanation2",
    placeholder="예: 같은 장르에서도 영화별 총 관객 수에 차이가 있다."
)


# ==========================================
# 그래프 3
# 총 관객 수 분포
# ==========================================
st.divider()
st.header("그래프 3. 영화별 총 관객 수 분포")

hist_df = df[
    ["movieNm", "total_audi"]
].copy()

hist_df = hist_df.dropna(
    subset=["movieNm", "total_audi"]
)

hist_df = hist_df[
    hist_df["total_audi"] >= 0
]

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 수 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    height=550
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

if len(hist_df) > 0:

    hist_df["구간"] = pd.cut(
        hist_df["total_audi"],
        bins=20,
        include_lowest=True
    )

    counts = hist_df["구간"].value_counts()

    if len(counts) > 0:

        most_common = counts.idxmax()

        st.write(
            f"영화가 가장 많이 몰린 구간은 "
            f"**약 {most_common.left:,.0f}명 ~ "
            f"{most_common.right:,.0f}명**입니다."
        )

    max_index = hist_df["total_audi"].idxmax()
    max_movie = hist_df.loc[max_index]

    st.write(
        f"가장 많은 관객을 기록한 영화는 "
        f"**「{max_movie['movieNm']}」**이며, "
        f"총 관객은 **{int(max_movie['total_audi']):,}명**입니다."
    )

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "그래프 3에서 알 수 있는 점을 한 문장으로 적어 보세요.",
    key="explanation3",
    placeholder="예: 영화별 총 관객 수는 특정 구간에 많이 몰려 있다."
)


# ==========================================
# 그래프 4
# 개봉일 스크린 수와 총 관객의 관계
# ==========================================
st.divider()
st.header("그래프 4. 개봉일 스크린 수와 총 관객의 관계")

scatter_df = df[
    ["movieNm", "genre", "first_scrn", "total_audi"]
].copy()

scatter_df = scatter_df.dropna(
    subset=[
        "movieNm",
        "genre",
        "first_scrn",
        "total_audi"
    ]
)

scatter_df = scatter_df[
    (scatter_df["first_scrn"] >= 0)
    & (scatter_df["total_audi"] >= 0)
]

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르"
    }
)

fig4.update_traces(
    marker=dict(
        size=9,
        opacity=0.75
    )
)

fig4.update_layout(
    height=650
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "그래프 4에서 알 수 있는 점을 한 문장으로 적어 보세요.",
    key="explanation4",
    placeholder="예: 개봉일 스크린 수와 총 관객 사이의 관계를 확인할 수 있다."
)


# ==========================================
# 그래프 5
# 장르별 총 관객 분포
# ==========================================
st.divider()
st.header("그래프 5. 장르별 총 관객 분포")

box_df = df[
    ["movieNm", "genre", "total_audi"]
].copy()

box_df = box_df.dropna(
    subset=[
        "movieNm",
        "genre",
        "total_audi"
    ]
)

box_df = box_df[
    box_df["total_audi"] >= 0
]

genre_counts = box_df["genre"].value_counts()

valid_genres = genre_counts[
    genre_counts >= 10
].index.tolist()

box_df = box_df[
    box_df["genre"].isin(valid_genres)
]

if len(box_df) > 0:

    fig5 = px.box(
        box_df,
        x="genre",
        y="total_audi",
        color="genre",
        points="outliers",
        hover_name="movieNm",
        title="영화가 10편 이상인 장르별 총 관객 분포",
        labels={
            "genre": "장르",
            "total_audi": "총 관객 수"
        }
    )

    fig5.update_layout(
        height=650,
        showlegend=False
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

else:
    st.warning("10편 이상의 영화가 있는 장르가 없습니다.")

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "그래프 5에서 알 수 있는 점을 한 문장으로 적어 보세요.",
    key="explanation5",
    placeholder="예: 장르에 따라 총 관객의 중앙값과 분포 범위가 다르게 나타난다."
)


# ==========================================
# 그래프 6
# 첫 주 관객 버블 그래프
# ==========================================
st.divider()
st.header("그래프 6. 첫 주 관객을 나타낸 버블 그래프")

bubble_df = df[
    [
        "movieNm",
        "genre",
        "first_scrn",
        "total_audi",
        "first_week_audi"
    ]
].copy()

bubble_df = bubble_df.dropna(
    subset=[
        "movieNm",
        "genre",
        "first_scrn",
        "total_audi",
        "first_week_audi"
    ]
)

bubble_df = bubble_df[
    (bubble_df["first_scrn"] >= 0)
    & (bubble_df["total_audi"] >= 0)
    & (bubble_df["first_week_audi"] >= 0)
]

if len(bubble_df) > 0:

    fig6 = px.scatter(
        bubble_df,
        x="first_scrn",
        y="total_audi",
        size="first_week_audi",
        color="genre",
        hover_name="movieNm",
        size_max=45,
        title="개봉일 스크린 수와 총 관객의 관계",
        labels={
            "first_scrn": "개봉일 스크린 수",
            "total_audi": "총 관객 수",
            "first_week_audi": "첫 주 관객",
            "genre": "장르"
        }
    )

    fig6.update_traces(
        marker=dict(
            opacity=0.7
        )
    )

    fig6.update_layout(
        height=700
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

else:
    st.warning("버블 그래프를 그릴 수 있는 데이터가 없습니다.")

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "그래프 6에서 알 수 있는 점을 한 문장으로 적어 보세요.",
    key="explanation6",
    placeholder="예: 첫 주 관객이 많은 영화일수록 버블의 크기가 크게 나타난다."
)


# ==========================================
# 그래프 7
# 제작 국가 → 장르 선버스트
# ==========================================
st.divider()
st.header("그래프 7. 제작 국가와 장르별 영화 편수")

sunburst_df = df[
    ["nation", "genre"]
].copy()

# 결측값 처리
sunburst_df["nation"] = (
    sunburst_df["nation"]
    .fillna("미상")
    .astype(str)
    .str.strip()
)

sunburst_df["genre"] = (
    sunburst_df["genre"]
    .fillna("미상")
    .astype(str)
    .str.strip()
)

# 빈 문자열 처리
sunburst_df.loc[
    sunburst_df["nation"] == "",
    "nation"
] = "미상"

sunburst_df.loc[
    sunburst_df["genre"] == "",
    "genre"
] = "미상"

# 국가 × 장르별 영화 편수 계산
sunburst_count = (
    sunburst_df
    .groupby(
        ["nation", "genre"],
        as_index=False
    )
    .size()
)

sunburst_count = sunburst_count.rename(
    columns={"size": "영화 편수"}
)

if len(sunburst_count) > 0:

    fig7 = px.sunburst(
        sunburst_count,
        path=["nation", "genre"],
        values="영화 편수",
        title="제작 국가 → 장르별 영화 편수"
    )

    fig7.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "영화 편수: %{value}편"
            "<extra></extra>"
        )
    )

    fig7.update_layout(
        height=700
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

else:
    st.warning("선버스트 그래프를 그릴 수 있는 데이터가 없습니다.")

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "그래프 7에서 알 수 있는 점을 한 문장으로 적어 보세요.",
    key="explanation7",
    placeholder="예: 제작 국가에 따라 영화 장르의 구성과 영화 편수가 다르게 나타난다."
)
