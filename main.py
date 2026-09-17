# =======================================
# 그래프 5. 장르별 총 관객 상자 그림
# =======================================
st.divider()
st.header("그래프 5. 장르별 총 관객 분포")

box_df = df[
    ["movieNm", "genre", "total_audi"]
].copy()

# 필요한 데이터가 없는 행 제거
box_df = box_df.dropna(
    subset=["movieNm", "genre", "total_audi"]
)

# 장르별 영화 편수 계산
genre_movie_count = box_df["genre"].value_counts()

# 영화가 10편 이상인 장르만 선택
valid_genres = genre_movie_count[
    genre_movie_count >= 10
].index

box_df = box_df[
    box_df["genre"].isin(valid_genres)
]

# 장르별 상자 그림
fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    title="영화가 10편 이상인 장르별 총 관객 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수"
    },
    custom_data=["movieNm"]
)

# 마우스를 올렸을 때 영화명이 보이도록 설정
fig5.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    height=650,
    showlegend=False
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.markdown("### 이 그래프로 알 수 있는 것")
st.text_input(
    "장르별 총 관객 상자 그림에서 알 수 있는 점을 한 문장으로 적어 보세요.",
    placeholder="예: 장르에 따라 총 관객의 분포와 영화 간 차이가 다르게 나타난다.",
    key="explanation5"
)
