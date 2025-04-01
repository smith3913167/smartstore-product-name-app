# keyword_analyzer.py
import pandas as pd
from naver_ad_api import get_related_keywords

def analyze_keywords(main_keyword):
    raw_keywords = get_related_keywords(main_keyword)

    data = []
    for item in raw_keywords:
        keyword = item.get("relKeyword")
        monthly_pc = int(item.get("monthlyPcQcCnt", 0))
        monthly_mobile = int(item.get("monthlyMobileQcCnt", 0))
        comp_level = item.get("compIdx", 0)  # 0~1 사이 값
        bid = int(item.get("bidAmt", 0)) if item.get("bidAmt") else 0
        prod_cnt = int(item.get("productCount", 0)) if item.get("productCount") else 0
        avg_price = int(item.get("avgProductPrice", 0)) if item.get("avgProductPrice") else 0

        total_search = monthly_pc + monthly_mobile
        score = (total_search * 0.5) + ((1 - comp_level) * 100) + (bid * 0.1)

        data.append({
            "키워드": keyword,
            "월간 검색량": total_search,
            "경쟁강도": comp_level,
            "광고비용": bid,
            "상품 수": prod_cnt,
            "평균가": avg_price,
            "종합 점수": round(score, 2)
        })

    df = pd.DataFrame(data)
    df = df.sort_values("종합 점수", ascending=False).reset_index(drop=True)
    return df