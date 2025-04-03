import requests
import streamlit as st
from urllib.parse import quote

def map_keyword_to_categories(main_keyword, related_keywords):
    try:
        all_keywords = [main_keyword] + related_keywords
        mapped_categories = []

        for keyword in all_keywords:
            encoded = quote(keyword)
            url = f"https://openapi.naver.com/v1/search/shop.json?query={encoded}&display=1"

            headers = {
                "X-Naver-Client-Id": st.secrets["NAVER_CLIENT_ID"],
                "X-Naver-Client-Secret": st.secrets["NAVER_CLIENT_SECRET"]
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                items = response.json().get("items", [])
                if items:
                    title = items[0].get("title", "")
                    category = items[0].get("category3") or items[0].get("category2") or items[0].get("category1")
                    if category:
                        mapped_categories.append(category)
            else:
                st.warning(f"🔍 카테고리 검색 실패 ({keyword}): {response.status_code}")

        return mapped_categories

    except Exception as e:
        st.error(f"❌ 카테고리 매핑 오류: {e}")
        return []
