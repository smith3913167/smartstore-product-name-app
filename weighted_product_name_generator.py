def generate_weighted_product_names(df, top_n=5):
    # 점수: 검색량↑, 경쟁률↓, 광고비↓
    df = df.copy()
    df["점수"] = (
        (df["검색량"] / df["검색량"].max()) * 0.5 +
        (1 - df["경쟁률"] / df["경쟁률"].max()) * 0.3 +
        (1 - df["광고비"] / df["광고비"].max()) * 0.2
    )
    df = df.sort_values("점수", ascending=False)

    # 상위 점수 키워드 조합하여 상품명 생성
    suggestions = [f"{row['키워드']} 베스트 아이템" for _, row in df.head(top_n).iterrows()]
    return suggestions, df