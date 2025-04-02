import pandas as pd
from io import BytesIO

def save_analysis_and_suggestions_to_excel(df: pd.DataFrame, suggestions_df: pd.DataFrame) -> BytesIO:
    """
    키워드 분석 결과(df)와 추천 상품명(suggestions_df)을 Excel로 저장하여 BytesIO 객체로 반환
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # 첫 번째 시트: 키워드 분석 결과
        df.to_excel(writer, index=False, sheet_name="키워드 분석 결과")

        # 두 번째 시트: 추천 상품명
        if not suggestions_df.empty:
            suggestions_df.to_excel(writer, index=False, sheet_name="추천 상품명")
        else:
            empty_df = pd.DataFrame({"안내": ["추천된 상품명이 없습니다."]})
            empty_df.to_excel(writer, index=False, sheet_name="추천 상품명")

    output.seek(0)
    return output