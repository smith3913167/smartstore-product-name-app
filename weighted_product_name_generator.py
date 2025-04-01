import pandas as pd

def generate_weighted_ranked_product_names(df, main_keyword):
    suggestions = []

    for _, row in df.iterrows():
        keyword = row["키워드"]
        bid = row.get("광고비", 0)
        avg_price = row.get("평균가", 0)

        name = f"{main_keyword} {keyword}"
        if bid > 300:
            name += " 프리미엄"
        elif avg_price < 10000:
            name += " 가성비"

        suggestions.append({
            "추천 상품명": name,
            "연관 키워드": keyword,
            "광고비": bid,
            "평균가": avg_price,
            "점수": row["종합 점수"]
        })

    return pd.DataFrame(suggestions).sort_values("점수", ascending=False).reset_index(drop=True)