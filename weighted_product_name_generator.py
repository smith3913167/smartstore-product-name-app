def generate_weighted_ranked_product_names(main_keyword, df):
    weighted = []
    for _, row in df.iterrows():
        score = row["월간 검색량(합산)"]
        if row["경쟁강도"] == "높음":
            score *= 0.8
        elif row["경쟁강도"] == "중간":
            score *= 1.0
        else:  # 낮음
            score *= 1.2
        weighted.append((row["키워드"], score))

    weighted.sort(key=lambda x: x[1], reverse=True)
    suggestions = []
    for i, (kw, _) in enumerate(weighted):
        if kw != main_keyword:
            suggestions.append(f"{main_keyword} {kw.replace(main_keyword, '').strip()}")
        if len(suggestions) >= 5:
            break

    return suggestions