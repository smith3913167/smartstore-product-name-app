import pandas as pd
from naver_api import get_related_keywords, get_keyword_data

# 키워드 분석 함수
def analyze_keywords(main_keyword):
    related_keywords = [main_keyword] + get_related_keywords(main_keyword)
    result = []

    for kw in related_keywords:
        data = get_keyword_data(kw)

        if not data or "results" not in data or not data["results"]:
            result.append({
                "키워드": kw,
                "월간 검색량(합산)": 0,
                "카테고리 일치": "Y",
                "경쟁강도": "중간"
            })
            continue

        monthly_search = sum(item['ratio'] for item in data['results'][0]['data'])

        result.append({
            "키워드": kw,
            "월간 검색량(합산)": round(monthly_search),
            "카테고리 일치": "Y",
            "경쟁강도": "중간"
        })

    df = pd.DataFrame(result)
    df = df.sort_values(by="월간 검색량(합산)", ascending=False).reset_index(drop=True)
    return df