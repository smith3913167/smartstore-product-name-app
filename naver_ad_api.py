import requests
import streamlit as st
import time
import hashlib
import hmac
import base64
import json

# ✅ 네이버 검색광고 API 환경 변수
BASE_URL = "https://api.naver.com"
API_KEY = st.secrets["NAVER_AD_API_KEY"]
SECRET_KEY = st.secrets["NAVER_AD_SECRET_KEY"]
CUSTOMER_ID = st.secrets["NAVER_CUSTOMER_ID"]

# ✅ Signature 생성 함수
def generate_signature(timestamp, method, uri, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    signature = hmac.new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode()

# ✅ 연관 키워드 가져오기 함수
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

        # ✅ 인코딩 지정 (중요!)
        response.encoding = response.apparent_encoding

        # ✅ 강제 디코딩 → JSON 파싱
        data = json.loads(response.text)

        if "keywordList" in data:
            return data["keywordList"]
        else:
            st.warning("⚠️ 키워드 데이터가 없습니다.")
            return []
    except Exception as e:
        st.error(f"❌ 검색 광고 API 요청 실패: {e}")
        return []