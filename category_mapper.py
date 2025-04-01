def guess_category(keyword):
    keyword = keyword.lower()

    category_dict = {
        "선풍기": "생활가전 > 계절가전 > 선풍기",
        "충전기": "디지털/가전 > 모바일액세서리 > 충전기",
        "멀티탭": "디지털/가전 > 전기용품 > 멀티탭",
        "usb": "디지털/가전 > 저장장치 > USB",
        "무선": "디지털/가전 > 모바일액세서리 > 무선기기",
        "젠더": "디지털/가전 > 모바일액세서리 > 젠더"
    }

    for key in category_dict:
        if key in keyword:
            return category_dict[key]

    return "기타 (수동 확인 필요)"