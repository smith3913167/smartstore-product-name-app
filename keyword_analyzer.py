import pandas as pd
from naver_ad_api import get_related_keywords

def analyze_keywords(main_keyword):
    raw_keywords = get_related_keywords(main_keyword)
    
    related_keywords = []
    data = []

    for keyword_info in raw_keywords:
        try:
            keyword = keyword_info.get("relKeyword", keyword_info.get("keyword"))
            related_keywords.append(keyword)

            monthly_pc = int(keyword_info.get("monthlyPcQcCnt", 0).replace(",", ""))
            monthly_mobile = int(keyword_info.get("monthlyMobileQcCnt", 0).replace(",", ""))
            total_search = monthly_pc + monthly_mobile

            comp_idx_raw = keyword_info.get("compIdx", "0")
            if comp_idx_raw in ["높음", "중간", "낮음"]:
                comp_map = {"낮음": 0.2, "중간": 0.5, "높음": 0.8}
                comp_idx = comp_map.get(comp_idx_raw, 0.5)
            else:
                comp_idx = float(comp_idx_raw)

            bid_amt_raw = keyword_info.get("bidAmt", "0")
            ad_price = 0 if bid_amt_raw in ["-", "< 10", None] else int(str(bid_amt_raw).replace(",", "").replace("< 10", "10"))

            product_count = int(str(keyword_info.get("productCount", 0)).replace(",", "").replace("< 10", "10"))
            avg_price = int(str(keyword_info.get("avgPrice", 0)).replace(",", "").replace("< 10", "10"))

            score = (
                (total_search / 1000) * 0.4 +
                (1 - comp_idx) * 100 * 0.3 +
                (1 / (product_count + 1)) * 10000 * 0.2 +
                (1 / (avg_price + 1)) * 100000 * 0.1
            )

            data.append({
                "키워드": keyword,
                "PC 검색량": monthly_pc,
                "모바일 검색량": monthly_mobile,
                "총 검색량": total_search,
                "경쟁도": comp_idx,
                "광고비": ad_price,
                "상품수": product_count,
                "평균가": avg_price,
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

    return df, related_keywords