def generate_weighted_ranked_product_names(df, max_items=5):
    if df.empty:
        return []

    sorted_df = df.sort_values(by="가중치점수", ascending=False).head(max_items)
    keyword = sorted_df.iloc[0]["키워드"].split()[0]  # 메인 키워드 기반

    names = []
    for i, row in sorted_df.iterrows():
        base = row["키워드"]
        if "추천" in base or "순위" in base:
            name = f"{base} 베스트 아이템"
        elif "비교" in base:
            name = f"{keyword} vs {base} 비교!"
        elif "후기" in base:
            name = f"{base} 리뷰 인기 제품"
        else:
            name = f"{base} 어떤 제품이 좋을까?"

        names.append(name)

    return {"추천 상품명": names}