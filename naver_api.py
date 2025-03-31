import requests
import os
from dotenv import load_dotenv

# .env 파일에서 API 키 불러오기
load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

def get_related_keywords(keyword):
    # 예시 연관 키워드 10개
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

def get_keyword_data(keyword):
    url = "https://openapi.naver.com/v1/datalab/search"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json"
    }

    body = {
        "startDate": "2024-02-01",
        "endDate": "2025-02-01",
        "timeUnit": "month",
        "keywordGroups": [{"groupName": keyword, "keywords": [keyword]}],
        "device": "pc",
        "ages": ["2", "3", "4"],  # ✅ 정확한 연령코드로 수정!
        "gender": ""
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        return response.json()
    except Exception as e:
        print(f"❌ [API 오류] 키워드 '{keyword}' 요청 중 에러 발생: {e}")
        return {}
