import requests
import streamlit as st
from dotenv import load_dotenv
import os

# ✅ 로컬 실행 시 .env 파일에서 API 키 불러오기
load_dotenv()
client_id = st.secrets.get("NAVER_CLIENT_ID")
client_secret = st.secrets.get("NAVER_CLIENT_SECRET")

# ✅ 연관 키워드 리스트 생성
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

# ✅ 키워드별 검색량 데이터 요청 함수
def get_keyword_data(keyword):
    url = "https://openapi.naver.com/v1/datalab/search"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json"
    }

    body = {
        "startDate": "2024-03-01",
        "endDate": "2025-03-01",
        "timeUnit": "month",
        "keywordGroups": [
            {
                "groupName": keyword,
                "keywords": [keyword]
            }
        ],
        "device": "all"  # PC + 모바일 포함
        # gender와 ages는 전체 대상으로 생략
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        # ✅ 디버깅용 전체 응답 출력
        st.write(f"🔍 [DEBUG] '{keyword}' 응답:", data)

        if "results" in data and data["results"][0].get("data") == []:
            st.warning(f"❗ '{keyword}'에 대한 검색 결과가 없습니다.")
        return data

    except requests.exceptions.RequestException as e:
        st.error(f"❌ [API 오류] '{keyword}' 요청 실패: {e}")
        return {}