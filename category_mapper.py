import requests
import streamlit as st

def get_category_for_keyword(keyword: str) -> str:
    """
    입력된 키워드에 대해 스마트스토어의 대표 카테고리를 반환합니다.
    실제 데이터 기반이 아니라 샘플용 API or 예측 방식으로 구현.
    """
    try:
        # Naver 검색어 자동완성 기반 카테고리 예측 (실제 API 사용시 대체 필요)
        url = f"https://search.shopping.naver.com/api/search/category?query={keyword}"
        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            result = response.json()

            # 구조에 따라 파싱 (샘플 기준)
            if "category" in result and result["category"]:
                return result["category"][0].get("name", "카테고리 정보 없음")
            else:
                return "카테고리 정보 없음"
        else:
            return f"카테고리 조회 실패 (code: {response.status_code})"
    except Exception as e:
        st.warning(f"카테고리 분석 중 오류 발생: {e}")
        return "카테고리 정보 없음"