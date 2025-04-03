import requests
import pandas as pd
import streamlit as st
import time
import hmac
import hashlib
import base64
import json
from urllib.parse import quote

# Signature 생성 함수
def generate_signature(secret_key, timestamp, method, uri, body=""):
    message = f"{timestamp}.{method}.{uri}.{body}"
    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode('utf-8')

# 키워드 분석 함수 (POST 방식, UTF-8 안전 인코딩 포함)
def analyze_keywords(main_keyword):
    try:
        uri = "/keywordstool"
        method = "POST"
        timestamp = str(int(time.time() * 1000))

        body_dict = {
            "hintKeywords": [main_keyword],
            "showDetail": 1
        }
        body_str = json.dumps(body_dict, ensure_ascii=False)

        signature = generate_signature(
            st.secrets["NAVER_AD_SECRET_KEY"],
            timestamp,
            method,
            uri,
            body_str
        )

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "X-Timestamp": timestamp,
            "X-API-KEY": st.secrets["NAVER_AD_API_KEY"],
            "X-Customer": st.secrets["NAVER_CUSTOMER_ID"],
            "X-Signature": signature
        }

        url = f"https://api.searchad.naver.com{uri}"
        response = requests.post(url, headers=headers, data=body_str.encode("utf-8"))

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

        related_keywords = df["키워드"].tolist()[:10]  # 상위 10개 연관 키워드

        for col in ["검색량", "광고비", "상품수"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.fillna(0)
        return df, related_keywords

    except Exception as e:
        st.error(f"❌ 키워드 분석 중 오류 발생: {e}")
        return None, []
