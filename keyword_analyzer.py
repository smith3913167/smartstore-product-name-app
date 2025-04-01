import pandas as pd
from naver_ad_api import get_related_keywords

# 🔁 문자열 경쟁도 -> 숫자값 매핑 함수
def convert_comp_idx(value):
    mapping = {"낮음": 0.2, "중간": 0.5, "높음": 0.9}
    try:
        return float(value)
    except:
        return mapping.get(value, 0.0)

# 🔁 문자열 숫자 -> 정수값 변환 함수
def parse_int(value):
    try:
        return int(value.replace("<", "").replace(",", "").strip())
    except:
        return 0

def analyze_keywords(main_keyword):
    raw_keywords = get_related_keywords(main_keyword)
    data = []

    for keyword_info in raw_keywords:
        try:
            keyword = keyword_info.get("relKeyword", keyword_info.get("keyword"))
            monthly_pc = parse_int(keyword_info.get("monthlyPcQcCnt", 0))
            monthly_mobile = parse_int(keyword_info.get("monthlyMobileQcCnt", 0))
            total_search = monthly_pc + monthly_mobile

            comp_idx = convert_comp_idx(keyword_info.get("compIdx", 0))  # 경쟁도
            ad_price = parse_int(keyword_info.get("bidAmt", 0))
            product_count = parse_int(keyword_info.get("productCount", 0))
            avg_price = parse_int(keyword_info.get("avgPrice", 0))

            # 종합 점수 계산
            score = (
                (total_search / 1000) * 0.4
                + (1 - comp_idx) * 100 * 0.3
                + (1 / (product_count + 1)) * 10000 * 0.2
                + (1 / (avg_price + 1)) * 100000 * 0.1
            )

            data.append({
                "키워드": keyword,
                "PC 검색량": monthly_pc,
                "모바일 검색량": monthly_mobile,
                "총 검색량": total_search,
                "경쟁도": comp_idx,
                "광고 입찰가": ad_price,
                "상품 수": product_count,
                "평균 가격": avg_price,
                "종합 점수": round(score, 2)
            })

        except Exception as e:
            print(f"❌ 데이터 처리 오류: {e}")
            continue

    df = pd.DataFrame(data)

    if "종합 점수" in df.columns:
        df = df.sort_values("종합 점수", ascending=False).reset_index(drop=True)
    else:
        print("❌ '종합 점수' 컬럼이 없습니다.")

    return df