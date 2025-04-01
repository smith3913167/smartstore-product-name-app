# naver_ad_api.py
import requests
import json
import streamlit as st

BASE_URL = "https://api.naver.com"

API_KEY = st.secrets["NAVER_AD_API_KEY"]       # ✅ 검색광고 API 키
SECRET_KEY = st.secrets["NAVER_AD_SECRET_KEY"] # ✅ 검색광고 Secret
CUSTOMER_ID = st.secrets["NAVER_CUSTOMER_ID"]  # ✅ 고객 ID

HEADERS = {
    "X-API-KEY": API_KEY,
    "X-CUSTOMER": CUSTOMER_ID,
    "X-Timestamp": "",
    "X-Signature": "",
    "Content-Type": "application/json"
}

def get_related_keywords(main_keyword):
    # 가상 API 예시 URL - 실제 운영 시 정확한 endpoint 확인 필요
    url = f"{BASE_URL}/keywordstool"
    params = {
        "hintKeywords": main_keyword,
        "showDetail": 1
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        result = response.json()
        return result.get("keywordList", [])
    except Exception as e:
        st.error(f"❌ 연관 키워드 요청 실패: {e}")
        return []