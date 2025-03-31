def generate_weighted_ranked_product_names(df):
    # 경쟁강도 점수 매핑 (낮음이 점수 높음)
    competition_score_map = {"낮음": 3, "중간": 2, "높음": 1}

    # 결측값 제거 및 타입 변환
    df = df.dropna(subset=["월간 검색량(합산)", "경쟁강도"])
    df["월간 검색량(합산)"] = df["월간 검색량(합산)"].astype(float)
    df["경쟁강도 점수"] = df["경쟁강도"].map(competition_score_map)

    # 가중치 점수 계산 (검색량 60%, 경쟁강도 40%)
    df["가중치 점수"] = df["월간 검색량(합산)"] * 0.6 + df["경쟁강도 점수"] * 100 * 0.4

    # 점수 기준으로 정렬
    df_sorted = df.sort_values(by="가중치 점수", ascending=False)

    # 상위 키워드 추출
    top_keywords = df_sorted["키워드"].head(3).tolist()
    main_keyword = top_keywords[0] if top_keywords else "인기상품"

    # 상품명 추천 리스트 생성
    suggestions = [
        f"{main_keyword} 베스트 아이템",
        f"{main_keyword} 인기 추천",
        f"{main_keyword} vs {top_keywords[1]}" if len(top_keywords) > 1 else f"{main_keyword} 비교 분석",
        f"{main_keyword} 특가 모음",
        f"{main_keyword} 어떤 제품이 좋을까?",
    ]

    return suggestions