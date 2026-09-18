# --------------------------------------------------
# 그래프 6. 첫 주 관객을 버블 크기로 나타낸 그래프
# --------------------------------------------------
st.divider()
st.header("그래프 6. 첫 주 관객을 나타낸 버블 그래프")

bubble_df = df[
    ["movieNm", "genre", "first_scrn", "total_audi", "first_week_audi"]
].copy()

# 필요한 데이터가 없는 행 제거
bubble_df = bubble_df.dropna(
    subset=["movieNm", "genre", "first_scrn", "total_audi", "first_week_audi"]
)

# 음수 데이터 제거
bubble_df = bubble_df[
    (bubble_df["first_scrn"] >= 0)
    & (bubble_df["total_audi"] >= 0)
    & (bubble_df["first_week_audi"] >= 0)
]

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=50,
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
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,}개<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{marker.size:,}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    height=700,
    legend_title="장르"
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_input(
    "첫 주 관객을 나타낸 버블 그래프에서 알 수 있는 점을 한 문장으로 적어 보세요.",
    placeholder="예: 첫 주 관객이 많은 영화는 버블의 크기가 크게 나타난다.",
    key="explanation6"
)
