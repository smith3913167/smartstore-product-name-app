import requests
import streamlit as st

def map_keyword_to_categories(keyword):
    try:
        # 네이버 검색광고 API 설정
        base_url = "https://api.naver.com"
        endpoint = "/keywordstool"
        url = f"{base_url}{endpoint}"

        headers = {
            "X-API-KEY": st.secrets["NAVER_AD_API_KEY"],
            "Content-Type": "application/json",
        }

        params = {
            "hintKeywords": keyword,
            "showDetail": 1
        }

        response = requests.get(url, headers=headers, params=params)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            st.warning(f"카테고리 분석 API 요청 실패: {response.text}")
            return ["카테고리 정보 없음"]

        data = response.json()
        keyword_list = data.get("keywordList", [])

        if not keyword_list:
            return ["카테고리 정보 없음"]

        # 카테고리 필드를 추정 (여기서는 relKeyword 기준 예시)
        categories = []
        for kw in keyword_list:
            rel_kw = kw.get("relKeyword")
            if rel_kw and rel_kw != keyword:
                categories.append(rel_kw)

        return categories[:5] if categories else ["카테고리 정보 없음"]

    except Exception as e:
        st.error(f"카테고리 매핑 중 오류 발생: {e}")
        return ["카테고리 정보 없음"]