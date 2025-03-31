import requests
import streamlit as st

# Streamlit Cloud에서 secrets.toml 값 불러오기
client_id = st.secrets["NAVER_CLIENT_ID"]
client_secret = st.secrets["NAVER_CLIENT_SECRET"]

# 연관 키워드 생성
def get_related_keywords(keyword):
    return [
        f"{keyword} 추천",
        f"{keyword} 인기",
        f"{keyword} 비교",
        f"{keyword} 저렴한",
        f"{keyword} 고속",
        f"{keyword} 차량용",
        f"{keyword} 브랜드",
        f"{keyword} 순위",
        f"{keyword} 후기",
        f"{keyword} 정품"
    ]

# 키워드별 검색량 분석
def get_keyword_data(keyword):
    url = "https://openapi.naver.com/v1/datalab/search"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json"
    }

    body = {
        "startDate": "2024-02-01",
        "endDate": "2025-02-01",
        "timeUnit": "month",
        "keywordGroups": [{"groupName": keyword, "keywords": [keyword]}],
        "device": "all",
        "gender": ""
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        # 검색결과 없을 때
        if "results" in data and data["results"][0].get("data") == []:
            st.warning(f"🔍 '{keyword}'에 대한 검색 결과가 없습니다.")
        return data

    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ [API 오류] '{keyword}' 요청 실패: {http_err}")
        return {}

    except Exception as e:
        st.error(f"❌ [예상치 못한 오류] '{keyword}': {e}")
        return {}