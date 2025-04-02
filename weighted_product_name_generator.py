import pandas as pd

def generate_weighted_ranked_product_names(df: pd.DataFrame, main_keyword: str) -> pd.DataFrame:
    """
    분석된 키워드 데이터를 기반으로 가중치를 적용해 상품명을 추천합니다.
    """
    product_names = []
    
    for _, row in df.iterrows():
        keyword = row["키워드"]
        search_volume = row["검색량"]
        ad_cost = row["광고비"]
        product_count = row["상품수"]

        # 가중치 기반 점수 계산
        score = (
            (search_volume / 1000) * 0.5 +
            (1 / (ad_cost + 1)) * 5000 * 0.3 +
            (1 / (product_count + 1)) * 10000 * 0.2
        )

        # 상품명 후보 생성
        product_name = f"{main_keyword} {keyword}"
        product_names.append({
            "추천 상품명": product_name,
            "점수": round(score, 2),
            "검색량": search_volume,
            "광고비": ad_cost,
            "상품수": product_count,
        })

    # 점수 기준으로 정렬
    suggestions_df = pd.DataFrame(product_names)
    suggestions_df = suggestions_df.sort_values("점수", ascending=False).reset_index(drop=True)

    return suggestions_df