import requests
import streamlit as st
from dotenv import load_dotenv

# .env 파일에서 환경변수 불러오기
load_dotenv()

# Streamlit Cloud용 secrets.toml에서 NAVER API 키 불러오기
client_id = st.secrets["NAVER_CLIENT_ID"]
client_secret = st.secrets["NAVER_CLIENT_SECRET"]

# 연관 키워드 리스트 생성
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

# 키워드별 검색량 데이터 요청 함수
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
        "keywordGroups": [
            {
                "groupName": keyword,
                "keywords": [keyword]
            }
        ],
        "device": "all",  # ✅ PC+모바일 검색 포함
        # "ages": ["20", "30", "40"],  # ❌ 전체 연령 사용 시 생략
        "gender": ""  # 전체 성별
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        data = response.json()

        # 검색 결과가 없을 경우 경고 메시지 출력
        if "results" in data and data["results"][0].get("data") == []:
            st.warning(f"❗ '{keyword}'에 대한 검색 결과가 없습니다.")
        return data

    except Exception as e:
        st.error(f"❌ [API 오류] '{keyword}' 요청 중 에러 발생: {e}")
        return {}