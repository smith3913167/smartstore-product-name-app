# category_mapper.py

def map_keyword_to_categories(keyword):
    """
    간단한 키워드 기반 카테고리 추론 함수 (실제 스마트스토어 데이터 기반 아님, 샘플 로직)
    향후 실제 네이버 카테고리 매핑 로직이나 DB 연동으로 개선 가능
    """
    keyword = keyword.lower()
    
    if "선풍기" in keyword:
        return ["가전 > 계절가전 > 선풍기", "가전 > 소형가전"]
    elif "충전기" in keyword:
        return ["디지털 > 스마트기기 > 충전기/케이블", "디지털 > 모바일기기"]
    elif "멀티탭" in keyword:
        return ["생활/주방 > 전기용품 > 멀티탭"]
    elif "이어폰" in keyword:
        return ["디지털 > 음향기기 > 이어폰", "디지털 > 모바일기기"]
    else:
        return ["기타"]