# weighted_product_name_generator.py

def generate_weighted_ranked_product_names(df, main_keyword):
    weighted_scores = []

    for _, row in df.iterrows():
        score = 0
        # 검색량 기반 가중치 (비율 70%)
        score += row["월간 검색량(합산)"] * 0.7

        # 경쟁 강도 기반 가중치 (비율 30%)
        if row["경쟁강도"] == "낮음":
            score += 100
        elif row["경쟁강도"] == "중간":
            score += 50
        else:  # 높음
            score += 20

        weighted_scores.append(score)

    # 점수 열 추가
    df["score"] = weighted_scores

    # 검색량이 있는 키워드만 필터링
    df_filtered = df[df["월간 검색량(합산)"] > 0]
    df_sorted = df_filtered.sort_values(by="score", ascending=False)

    # 상위 키워드 추출
    top_keywords = df_sorted.head(3)["키워드"].tolist()

    product_names = []
    if top_keywords:
        for kw in top_keywords:
            # 메인 키워드 제외 후 나머지만 조합
            suffix = kw.replace(main_keyword, '').strip()
            name = f"{main_keyword} {suffix}" if suffix else main_keyword
            product_names.append(name.strip())
    else:
        # 기본 백업 상품명
        product_names = [f"{main_keyword} 추천", f"{main_keyword} 인기 상품"]

    # 순위 부여 및 딕셔너리 형태로 반환
    ranked = [{"순위": i + 1, "상품명": name} for i, name in enumerate(product_names)]
    return ranked
