import pandas as pd

def analyze_keywords_pandarank_style(keywords):
    data = []
    for keyword in keywords:
        # 샘플 데이터 생성 (실제 API 데이터로 대체 가능)
        monthly_search = max(1000 - hash(keyword) % 500, 100)  # 검색량
        product_count = max(10000 - hash(keyword[::-1]) % 5000, 500)  # 상품 수
        ad_cost = max(100 + hash(keyword + "ad") % 1000, 50)  # 광고비
        conversion_rate = round(1 + hash(keyword + "conv") % 100 / 100, 2)  # 전환율
        avg_price = max(10000 + hash(keyword + "price") % 90000, 5000)

        # 경쟁률 계산: 상품 수 / 검색량 (낮을수록 좋음)
        competition = round(product_count / monthly_search, 2)

        data.append({
            "키워드": keyword,
            "검색량": monthly_search,
            "상품수": product_count,
            "경쟁률": competition,
            "전환율": conversion_rate,
            "광고비": ad_cost,
            "평균가": avg_price
        })

    df = pd.DataFrame(data)
    return df