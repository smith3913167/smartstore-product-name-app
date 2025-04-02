import requests
import pandas as pd
import streamlit as st

def analyze_keywords(main_keyword):
    try:
        # 1. JSON 페이로드 구성
        payload = {
            "hintKeywords": main_keyword,
            "showDetail": 1
        }

        # 2. 헤더 설정 (Content-Type 꼭 명시)
        headers = {
            "X-API-KEY": st.secrets["NAVER_API_KEY"],
            "Content-Type": "application/json; charset=utf-8"
        }

        # 3. POST 요청 (data가 아닌 json= 사용)
        response = requests.post(
            "https://api.naver.com/keywordstool",
            headers=headers,
            json=payload  # ⚠️ UTF-8 자동 인코딩
        )

        response.encoding = 'utf-8'
        if response.status_code != 200:
            st.error(f"❌ 검색 광고 API 요청 실패: {response.text}")
            return None, []

        # 4. 응답 처리
        data = response.json()
        keywords_data = data.get("keywordList", [])

        if not keywords_data:
            return None, []

        df = pd.DataFrame(keywords_data)

        df = df.rename(columns={
            "relKeyword": "키워드",
            "monthlyPcQcCnt": "검색량",
            "compIdx": "경쟁 강도",
            "monthlyAvePcCtr": "평균 CTR",
            "monthlyAvePcCpc": "광고비",
            "productCnt": "상품수",
        })

        for col in ["검색량", "광고비", "상품수"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.fillna(0)
        related_keywords = df["키워드"].tolist()[:10]

        return df, related_keywords

    except Exception as e:
        st.error(f"❌ 키워드 분석 중 오류 발생: {e}")
        return None, []