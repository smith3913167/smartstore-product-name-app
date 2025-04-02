import requests
import pandas as pd
from urllib.parse import quote
import streamlit as st

def analyze_keywords(main_keyword):
    try:
        encoded_keyword = quote(main_keyword, encoding='utf-8')

        api_url = f"https://api.naver.com/keywordstool?hintKeywords={encoded_keyword}&showDetail=1"

        headers = {
            "X-API-KEY": st.secrets["NAVER_AD_API_KEY"],  # 수정된 부분
            "Content-Type": "application/json",
            "customerId": st.secrets["NAVER_CUSTOMER_ID"],  # 검색광고에선 보통 필요
        }

        response = requests.get(api_url, headers=headers)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            st.error(f"❌ 검색 광고 API 요청 실패: {response.text}")
            return None, []

        data = response.json()

        # 키워드 데이터 추출
        keywords_data = data.get("keywordList", [])

        if not keywords_data:
            return None, []

        df = pd.DataFrame(keywords_data)

        # 컬럼명 변환
        df = df.rename(columns={
            "relKeyword": "키워드",
            "monthlyPcQcCnt": "검색량",
            "compIdx": "경쟁 강도",
            "monthlyAvePcCtr": "평균 CTR",
            "monthlyAvePcCpc": "광고비",
            "productCnt": "상품수",
        })

        # 연관 키워드 상위 10개 추출
        related_keywords = df["키워드"].tolist()[:10]

        # 수치형 처리
        for col in ["검색량", "광고비", "상품수"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.fillna(0)

        return df, related_keywords

    except Exception as e:
        st.error(f"❌ 키워드 분석 중 오류 발생: {e}")
        return None, []