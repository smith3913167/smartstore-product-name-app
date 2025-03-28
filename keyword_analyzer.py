from naver_api import get_related_keywords, get_keyword_data
import pandas as pd

def analyze_keywords(main_keyword):
    related_keywords = get_related_keywords(main_keyword)
    all_keywords = [main_keyword] + related_keywords[:10]

    data = []

    for keyword in all_keywords:
        result = get_keyword_data(keyword)

        print(f"\n🔍 [DEBUG] 키워드: {keyword}")
        print(result)  # 응답 확인용

        # 네이버 API 응답에 'results'가 없으면 건너뜀
        if not result or 'results' not in result:
            print(f"⚠️ [무시됨] 키워드 '{keyword}'는 유효한 결과가 없습니다.")
            continue

        try:
            monthly_total = sum([x['ratio'] for x in result['results'][0]['data']])
        except Exception as e:
            print(f"❌ [오류] 키워드 '{keyword}' 처리 중 오류 발생: {e}")
            continue

        data.append({
            "키워드": keyword,
            "월간 검색량(합산)": int(monthly_total),
            "카테고리 일치": "Y" if main_keyword in keyword else "N",
            "경쟁강도": "중간"  # 향후 알고리즘 적용 가능
        })

    if data:
        return pd.DataFrame(data)
    else:
        print("❗ 유효한 데이터가 없습니다.")
        return pd.DataFrame(columns=["키워드", "월간 검색량(합산)", "카테고리 일치", "경쟁강도"])