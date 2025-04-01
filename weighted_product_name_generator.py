import random

def generate_weighted_ranked_product_names(df, main_keyword):
    suggestions = []
    
    prefixes = ["프리미엄", "고급형", "감성", "베스트", "핫한"]
    suffixes = ["추천", "세트", "구성", "컬렉션", "신상"]

    for _, row in df.iterrows():
        keyword = row["키워드"]
        score = row["종합 점수"]

        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)

        product_name = f"{prefix} {keyword} {suffix}"
        suggestions.append({
            "추천 상품명": product_name,
            "기준 키워드": keyword,
            "종합 점수": score
        })

    suggestion_df = (
        pd.DataFrame(suggestions)
        .sort_values("종합 점수", ascending=False)
        .reset_index(drop=True)
    )

    return suggestion_df