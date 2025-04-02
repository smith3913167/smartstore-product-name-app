import requests
import pandas as pd
from urllib.parse import quote
import streamlit as st

def analyze_keywords(main_keyword):
    try:
        encoded_keyword = quote(main_keyword)

        # 네이버 검색광고 API 엔드포인트 (POST 방식)
        url = "https://api.searchad.naver.com/keywordstool"

        headers = {
            "X-API-KEY": st.secrets["NAVER_AD_API_KEY"],
            "X-CUSTOMER": st.secrets["NAVER_CUSTOMER_ID"],
            "Content-Type": "application/json; charset=UTF-8"
        }

        payload = {
            "hintKeywords": [main_keyword],
            "showDetail": 1
        }

        response = requests.post(url, headers=headers, json=payload)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            st.error(f"❌검색 광고 API 요청 실패: {response.text}")
            return None, []

        data = response.json()
        keyword_list = data.get("keywordList", [])

        if not keyword_list:
            return None, []

        df = pd.DataFrame(keyword_list)

        df = df.rename(columns={
            "relKeyword": "키워드",
            "monthlyPcQcCnt": "검색량",
            "compIdx": "경쟁 강도",
            "monthlyAvePcCtr": "평균 CTR",
            "monthlyAvePcCpc": "광고비",
            "productCnt": "상품수",
        })

        # 숫자형 처리
        for col in ["검색량", "광고비", "상품수"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.fillna(0)
        df = df.sort_values(by="검색량", ascending=False)

        related_keywords = df["키워드"].tolist()[1:11]  # 입력 키워드 제외

        return df, related_keywords

    except Exception as e:
        st.error(f"❌ 키워드 분석 중 오류 발생: {e}")
        return None, []
