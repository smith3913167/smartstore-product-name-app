import requests
import time
import hmac
import hashlib
import base64
import streamlit as st
from urllib.parse import quote


def generate_signature(timestamp, method, uri, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    message_bytes = message.encode('utf-8')
    signing_key = secret_key.encode('utf-8')
    signature = hmac.new(signing_key, message_bytes, hashlib.sha256).digest()
    return base64.b64encode(signature).decode('utf-8')


def map_keyword_to_categories(keyword: str) -> list:
    try:
        # Secrets from .streamlit/secrets.toml or Streamlit Cloud
        api_key = st.secrets["NAVER_AD_API_KEY"]
        secret_key = st.secrets["NAVER_AD_SECRET_KEY"]
        customer_id = st.secrets["NAVER_CUSTOMER_ID"]

        timestamp = str(int(time.time() * 1000))
        method = "GET"
        uri = "/keywordstool"
        encoded_keyword = quote(keyword, safe='')

        query = f"hintKeywords={encoded_keyword}&showDetail=1"
        url = f"https://api.naver.com{uri}?{query}"

        signature = generate_signature(timestamp, method, uri, secret_key)

        headers = {
            "X-Timestamp": timestamp,
            "X-API-KEY": api_key,
            "X-Customer": customer_id,
            "X-Signature": signature,
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            st.error(f"❌ 카테고리 API 요청 실패: {response.text}")
            return []

        data = response.json()

        # 연관 키워드 중 카테고리명 유추
        keywords_data = data.get("keywordList", [])
        category_names = []

        for item in keywords_data:
            rel_keyword = item.get("relKeyword", "")
            if ">" in rel_keyword or "카테고리" in rel_keyword:
                category_names.append(rel_keyword)
            elif keyword in rel_keyword:
                category_names.append(rel_keyword)

        # 중복 제거 및 최대 5개 추출
        unique_categories = list(set(category_names))[:5]

        return unique_categories

    except Exception as e:
        st.error(f"❌ 카테고리 매핑 중 오류 발생: {e}")
        return []