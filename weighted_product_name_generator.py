import random

def generate_weighted_ranked_product_names(df, main_keyword):
    suggestions = []

    for _, row in df.iterrows():
        keyword = row["키워드"]
        score = row["종합 점수"]
        bid = row["광고 입찰가"]
        avg_price = row["평균 가격"]

        # 조합 요소 추출
        ad_tag = "인기" if bid > 100 else "가성비"
        price_tag = f"{avg_price//1000}천원대" if avg_price else "특가"
        base_name = f"{main_keyword} {keyword} {ad_tag} {price_tag}"

        # 랜덤 요소 추가
        suffix = random.choice(["추천", "TOP", "BEST", "정품", "브랜드"])
        full_name = f"{base_name} {suffix}"

        suggestions.append({
            "추천 상품명": full_name,
            "가중치 점수": round(score, 2),
            "연관 키워드": keyword,
            "광고비용": bid,
            "평균가": avg_price
        })

    # 종합 점수 기준 정렬 후 반환
    suggestions = sorted(suggestions, key=lambda x: x["가중치 점수"], reverse=True)

    return suggestions