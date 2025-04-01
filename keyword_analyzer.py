import pandas as pd

# 목업용 데이터 생성 함수
def analyze_keywords(base_keyword):
    keywords = [
        base_keyword,
        f"{base_keyword} 추천",
        f"{base_keyword} 고속",
        f"{base_keyword} 순위",
        f"{base_keyword} 인기",
        f"{base_keyword} 저렴한",
        f"{base_keyword} 비교",
        f"{base_keyword} 차량용",
        f"{base_keyword} 브랜드",
        f"{base_keyword} 후기",
        f"{base_keyword} 정품",
    ]

    # 검색량, 경쟁강도, 광고비, 상품수, 평균가 - 임의의 mock 데이터
    data = {
        "키워드": keywords,
        "월간 검색량(합산)": [856, 318, 100, 100, 0, 0, 0, 0, 0, 0, 0],
        "카테고리 일치": ["Y"] * len(keywords),
        "경쟁강도 점수": [52.3, 16.2, 1.5, 3.2, 39.4, 0.2, 0.2, 0.3, 0.3, 0.4, 0.5],
        "광고비": [820, 720, 310, 300, 600, 100, 150, 200, 250, 300, 180],
        "상품수": [3185586, 756334, 62537, 79615, 642097, 2686, 1013, 5000, 4200, 3800, 3000],
        "평균가": [57000, 58000, 38000, 149000, 108620, 39900, 39000, 42000, 45000, 46000, 47000],
    }

    df = pd.DataFrame(data)

    # 경쟁강도 구간 설정
    def classify_competition(score):
        if score >= 40:
            return "높음"
        elif score >= 10:
            return "중간"
        else:
            return "낮음"

    df["경쟁강도"] = df["경쟁강도 점수"].apply(classify_competition)

    return df