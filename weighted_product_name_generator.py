import pandas as pd

# 금지어 리스트 예시
FORBIDDEN_WORDS = ["최고", "싸다", "무료", "할인"]

# 경쟁강도 가중치
COMPETITION_WEIGHT = {
    "낮음": 1.0,
    "중간": 0.8,
    "높음": 0.5
}

def clean_keyword(base, keyword):
    word = keyword.replace(base, "").strip()
    for bad in FORBIDDEN_WORDS:
        if bad in word:
            return ""
    return word

def generate_weighted_ranked_product_names(df, max_names=5, max_length=30):
    if df.empty:
        return pd.DataFrame({"추천 순위": ["-"], "추천 상품명": ["⚠️ 유효한 키워드가 없습니다."]})

    # 가중치 점수 계산
    df["가중치 점수"] = df.apply(
        lambda row: row["월간 검색량(합산)"] * COMPETITION_WEIGHT.get(row["경쟁강도"], 0.7),
        axis=1
    )

    df_sorted = df[df["월간 검색량(합산)"] > 0].sort_values(by="가중치 점수", ascending=False).reset_index(drop=True)

    if df_sorted.empty:
        return pd.DataFrame({"추천 순위": ["-"], "추천 상품명": ["⚠️ 유효한 키워드가 없습니다."]})

    core = df_sorted.iloc[0]["키워드"]
    features = []

    for i in range(1, len(df_sorted)):
        cleaned = clean_keyword(core, df_sorted.iloc[i]["키워드"])
        if cleaned and cleaned not in features:
            features.append(cleaned)
        if len(features) >= max_names * 2:
            break

    product_names = []
    for i in range(max_names):
        part1 = features[i] if i < len(features) else ""
        part2 = features[i + 1] if i + 1 < len(features) else ""
        name = f"{core} {part1} {part2}".strip()
        if len(name) <= max_length:
            product_names.append(name)

    # 순위화된 데이터프레임 반환
    ranked_df = pd.DataFrame({
        "추천 순위": [f"{i+1}위" for i in range(len(product_names))],
        "추천 상품명": product_names
    })

    return ranked_df
