# keyword_analyzer.py
import pandas as pd
import random

def analyze_keywords(main_keyword):
    related_keywords = [
        f"{main_keyword} 추천",
        f"{main_keyword} 인기",
        f"{main_keyword} 비교",
        f"{main_keyword} 저렴한",
        f"{main_keyword} 고속",
        f"{main_keyword} 차량용",
        f"{main_keyword} 브랜드",
        f"{main_keyword} 순위",
        f"{main_keyword} 후기",
        f"{main_keyword} 정품"
    ]

    results = []
    for kw in [main_keyword] + related_keywords:
        monthly_search = random.randint(0, 1000)
        category_match = 'Y'
        competition_score = round(random.uniform(0.1, 100), 2)
        ad_cost = random.randint(100, 1500)
        product_count = random.randint(1000, 100000)
        avg_price = random.randint(20000, 200000)

        if competition_score >= 60:
            competition_level = '높음'
        elif competition_score >= 30:
            competition_level = '중간'
        else:
            competition_level = '낮음'

        results.append({
            "키워드": kw,
            "월간 검색량(합산)": monthly_search,
            "카테고리 일치": category_match,
            "경쟁강도": competition_level,
            "광고비": ad_cost,
            "상품수": product_count,
            "평균가": avg_price
        })

    df = pd.DataFrame(results)
    return df