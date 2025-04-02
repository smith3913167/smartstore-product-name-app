import requests
import pandas as pd
import json
import streamlit as st
from urllib.parse import quote

def analyze_keywords(main_keyword):
    try:
        # 검색 키워드 인코딩
        encoded_keyword = quote(main_keyword)

        # 요청 데이터 생성
        payload = {
            "hintKeywords": main_keyword,
            "showDetail": 1
        }

        headers = {
            "X-API-KEY": st.secrets["NAVER_API_KEY"],
            "Content-Type": "application/json; charset=utf-8"
        }

        # API 호출 (중요: data가 아닌 json으로 전달)
        response = requests.post(
            "https://api.naver.com/keywordstool",
            headers=headers,
            json=payload  # ← json 인자로 넘기면 자동으로 utf-8 인코딩됨
        )

        response.encoding = 'utf-8'
        if response.status_code != 200:
            st.error(f"❌ 검색 광고 API 요청 실패: {response.text}")
            return None, []

        data = response.json()
        keywords_data = data.get("keywordList", [])

        if not keywords_data:
            return None, []

        df = pd.DataFrame(keywords_data)

        # 컬럼명 정리
        df = df.rename(columns={
            "relKeyword": "키워드",
            "monthlyPcQcCnt": "검색량",
            "compIdx": "경쟁 강도",
            "monthlyAvePcCtr": "평균 CTR",
            "monthlyAvePcCpc": "광고비",
            "productCnt": "상품수",
        })

        # 숫자형 변환
        for col in ["검색량", "광고비", "상품수"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.fillna(0)
        related_keywords = df["키워드"].tolist()[:10]

        return df, related_keywords

    except Exception as e:
        st.error(f"❌ 키워드 분석 중 오류 발생: {e}")
        return None, []
