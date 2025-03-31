import requests
import streamlit as st
from dotenv import load_dotenv

# .env 파일에서 API 키 불러오기
load_dotenv()

client_id = st.secrets["NAVER_CLIENT_ID"]
client_secret = st.secrets["NAVER_CLIENT_SECRET"]

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
        "device": "pc",
        "ages": ["20", "30", "40", "50"],  # ✅ 연령대 코드 수정
        "gender": ""  # or "m" / "f"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        result = response.json()

        # ✅ 예외 확인 및 로깅
        if 'results' not in result or not result['results'][0]['data']:
            st.warning(f"'{keyword}'에 대한 검색 결과가 없습니다.")
        return result

    except Exception as e:
        st.error(f"❌ [API 에러] 키워드 '{keyword}' 검색 중 오류 발생: {e}")
        return {}