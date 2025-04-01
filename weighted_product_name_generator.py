def generate_weighted_ranked_product_names(df):
    suggestions = []

    for _, row in df.iterrows():
        keyword = row["키워드"]
        volume = row.get("월간 검색량(합산)", 0)
        competition_score = row.get("경쟁강도 점수", 0)
        ad_cost = row.get("광고비", 0)
        product_count = row.get("상품수", 0)

        # 가중치 기반 점수 계산 (높을수록 유리한 방향)
        score = (
            (volume * 0.4) +               # 검색량
            (ad_cost * 0.3) +             # 광고비 (높을수록 인기)
            ((1 / (product_count + 1)) * 10000 * 0.2) +  # 상품 수 적을수록 유리
            ((1 / (competition_score + 1)) * 100 * 0.1)  # 경쟁강도 낮을수록 유리
        )

        suggestions.append((keyword, score))

    # 점수 기준 정렬
    ranked = sorted(suggestions, key=lambda x: x[1], reverse=True)

    # 상위 10개 상품명 반환
    return [kw for kw, _ in ranked[:10]]