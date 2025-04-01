import requests
import streamlit as st
import time
import hashlib
import hmac
import base64
import json

# ✅ 검색광고 API (SearchAD) 환경변수
BASE_URL = "https://api.naver.com"
API_KEY = st.secrets["NAVER_AD_API_KEY"]
SECRET_KEY = st.secrets["NAVER_AD_SECRET_KEY"]
CUSTOMER_ID = st.secrets["NAVER_CUSTOMER_ID"]  # 예: "2091030"

# 🔐 서명 생성 함수
def generate_signature(timestamp, method, uri, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    signature = hmac.new(
        bytes(secret_key, "utf-8"),
        bytes(message, "utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode()

# 🔍 연관 키워드 추출 함수 (예: 키워드 도출용)
def get_related_keywords(keyword):
    uri = "/keywordstool"
    method = "GET"
    timestamp = str(int(time.time() * 1000))
    signature = generate_signature(timestamp, method, uri, SECRET_KEY)

    headers = {
        "X-Timestamp": timestamp,
        "X-API-KEY": API_KEY,
        "X-Customer": CUSTOMER_ID,
        "X-Signature": signature,
    }

    params = {
        "hintKeywords": keyword,
        "showDetail": 1
    }

    try:
        response = requests.get(BASE_URL + uri, headers=headers, params=params)
        data = response.json()

        if "keywordList" in data:
            keywords = [item["relKeyword"] for item in data["keywordList"] if "relKeyword" in item]
            return list(set(keywords))[:10]  # 연관 키워드 상위 10개 반환
        else:
            st.warning("검색 광고 API에서 키워드를 찾을 수 없습니다.")
            return []
    except Exception as e:
        st.error(f"검색 광고 API 요청 실패: {e}")
        return []
