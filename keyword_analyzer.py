import requests
import pandas as pd
from urllib.parse import quote
import streamlit as st
import hashlib
import hmac
import base64
import time
import json

def analyze_keywords(main_keyword):
    try:
        timestamp = str(int(time.time() * 1000))
        base_url = "https://api.naver.com"
        uri = "/keywordstool"
        full_url = base_url + uri

        body = {
            "hintKeywords": [main_keyword],
            "siteId": None,
            "biztpId": None,
        }

        secret_key = bytes(st.secrets["NAVER_AD_SECRET_KEY"], 'utf-8')
        message = f"{timestamp}.{uri}.{json.dumps(body, ensure_ascii=False)}"
        signature = hmac.new(secret_key, message.encode('utf-8'), hashlib.sha256).digest()
        signature_base64 = base64.b64encode(signature).decode()

        headers = {
            "X-Timestamp": timestamp,
            "X-API-KEY": st.secrets["NAVER_AD_API_KEY"],
            "X-CUSTOMER": st.secrets["NAVER_CUSTOMER_ID"],
            "X-Signature": signature_base64,
            "Content-Type": "application/json",
        }

        # ✅ 핵심: json=body로 보내야 인코딩 오류 없음
        response = requests.post(full_url, headers=headers, json=body)

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