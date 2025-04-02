import time
import hmac
import hashlib
import base64
import pandas as pd
import requests
import streamlit as st

def generate_signature(timestamp, method, uri, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    signature = hmac.new(
        bytes(secret_key, "utf-8"),
        bytes(message, "utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode()

def analyze_keywords(main_keyword):
    try:
        uri = "/keywordstool"
        full_url = f"https://api.naver.com{uri}"

        timestamp = str(int(time.time() * 1000))
        method = "POST"
        secret_key = st.secrets["NAVER_AD_SECRET_KEY"]
        api_key = st.secrets["NAVER_AD_API_KEY"]
        customer_id = st.secrets["NAVER_CUSTOMER_ID"]

        signature = generate_signature(timestamp, method, uri, secret_key)

        headers = {
            "X-Timestamp": timestamp,
            "X-API-KEY": api_key,
            "X-Customer": customer_id,
            "X-Signature": signature,
            "Content-Type": "application/json"
        }

        body = {
            "hintKeywords": [main_keyword],
            "showDetail": 1
        }

        response = requests.post(full_url, headers=headers, json=body)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            st.error(f"❌ 검색 광고 API 요청 실패: {response.text}")
            return None, []

        data = response.json()
        keywords_data = data.get("keywordList", [])
        if not keywords_data:
            return None, []

        df = pd.DataFrame(keywords_data)

        df = df.rename(columns={
            "relKeyword": "키워드",
            "monthlyPcQcCnt": "검색량",
            "compIdx": "경쟁 강도",
            "monthlyAvePcCtr": "평균 CTR",
            "monthlyAvePcCpc": "광고비",
            "productCnt": "상품수",
        })

        related_keywords = df["키워드"].tolist()[:10]

        for col in ["검색량", "광고비", "상품수"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.fillna(0)

        return df, related_keywords

    except Exception as e:
        st.error(f"❌ 키워드 분석 중 오류 발생: {e}")
        return None, []