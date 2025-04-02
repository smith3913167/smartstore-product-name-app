# category_mapper.py
import time
import hmac
import hashlib
import base64
import requests
import json
import pandas as pd
import streamlit as st
from urllib.parse import quote

def get_signature(timestamp, method, uri, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    signing_key = bytes(secret_key, 'utf-8')
    message = bytes(message, 'utf-8')
    signature = hmac.new(signing_key, message, digestmod=hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

def map_keyword_to_categories(main_keyword):
    try:
        base_url = "https://api.naver.com"
        uri = "/keywordstool"
        method = "GET"

        timestamp = str(int(time.time() * 1000))
        encoded_keyword = quote(main_keyword, encoding='utf-8')
        params = f"hintKeywords={encoded_keyword}&showDetail=1"
        url = f"{base_url}{uri}?{params}"

        signature = get_signature(
            timestamp,
            method,
            uri,
            st.secrets["NAVER_AD_SECRET_KEY"]
        )

        headers = {
            "X-Timestamp": timestamp,
            "X-API-KEY": st.secrets["NAVER_AD_API_KEY"],
            "X-Customer": st.secrets["NAVER_CUSTOMER_ID"],
            "X-Signature": signature,
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            st.error(f"❌ API 요청 실패: {response.text}")
            return []

        data = response.json()
        keywords_data = data.get("keywordList", [])

        # 유사 키워드를 기반으로 카테고리 유추
        categories = []
        for item in keywords_data[:10]:
            keyword = item.get("relKeyword")
            if keyword:
                # 예시로 유사 키워드 자체를 "카테고리 후보"로 반환
                categories.append(keyword)

        return list(set(categories))  # 중복 제거

    except Exception as e:
        st.error(f"❌ 카테고리 추론 중 오류 발생: {e}")
        return []