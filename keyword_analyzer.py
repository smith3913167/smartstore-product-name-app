import requests
import pandas as pd
import streamlit as st
from naver_api import get_related_keywords, get_keyword_data

def analyze_keywords(main_keyword):
    keywords = [main_keyword] + get_related_keywords(main_keyword)
    data = []

    for kw in keywords:
        response = get_keyword_data(kw)
        monthly_volume = 0

        if "results" in response and response["results"]:
            monthly_data = response["results"][0].get("data", [])
            monthly_volume = sum(item["ratio"] for item in monthly_data)

        # 💡 PandaRank 스타일 mock 데이터
        category_match = "Y" if main_keyword in kw else "N"
        competition_level = "높음" if monthly_volume > 1000 else "중간" if monthly_volume > 100 else "낮음"
        competition_score = {"높음": 1.0, "중간": 0.5, "낮음": 0.2}[competition_level]
        ad_cost = int(monthly_volume * 12)  # 단순 비례 mock
        product_count = int(monthly_volume * 3) + 50  # mock
        average_price = 15000 + (monthly_volume % 5000)

        data.append({
            "키워드": kw,
            "검색량": int(monthly_volume),
            "카테고리일치": category_match,
            "경쟁강도": competition_level,
            "경쟁강도점수": competition_score,
            "광고비": ad_cost,
            "상품수": product_count,
            "평균가": average_price
        })

    df = pd.DataFrame(data)

    # 가중치 점수 계산
    df["가중치점수"] = (
        df["검색량"] * 0.4 +
        (1 - df["경쟁강도점수"]) * 1000 * 0.3 +
        (100000 - df["광고비"]) * 0.1 +
        (1000 / (df["상품수"] + 1)) * 100 * 0.2
    )

    df.sort_values(by="가중치점수", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df