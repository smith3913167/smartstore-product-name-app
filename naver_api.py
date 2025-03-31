import requests
import streamlit as st
from dotenv import load_dotenv
import os

# .env 파일에서 환경변수 불러오기 (로컬용)
load_dotenv()

# Streamlit Cloud에서는 secrets.toml 사용
client_id = st.secrets["NAVER_CLIENT_ID"]
client_secret = st.secrets["NAVER_CLIENT_SECRET"]

# 간단한 연관 키워드 만들기
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

# 키워드 검색량 데이터 통신

def get_keyword_data(keyword):
    url = "https://openapi.naver.com/v1/datalab/search"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json"
    }

    body = {
        "startDate": "2024-03-01",  # 유효한 날짜
        "endDate": "2025-02-28",
        "timeUnit": "month",
        "keywordGroups": [
            {
                "groupName": keyword,
                "keywords": [keyword]
            }
        ],
        "device": "pc",
        "gender": ""  # 성별 필수 X
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        if "results" in data and data["results"][0].get("data") == []:
            st.warning(f"\u26a0\ufe0f '{keyword}'\uc5d0 \ub300\ud55c \uac80\uc0c9 \uacb0\uacfc\uac00 \uc5c6\uc2b5\ub2c8\ub2e4.")
        return data

    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ [API \uc624\ub958] '{keyword}' \uc694\uccad \uc2e4\ud328: {http_err}")
    except Exception as e:
        st.error(f"❌ [\uc608외] '{keyword}' \uc694\uccad \uc911 \uc5d0\ub7ec \ubc1c생: {e}")

    return {}
