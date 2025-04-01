import pandas as pd
from io import BytesIO

def save_analysis_and_suggestions_to_excel(df, suggestions):
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # 키워드 분석 결과 시트 저장
        if df is not None and not df.empty:
            df.to_excel(writer, index=False, sheet_name='키워드 분석 결과')
        else:
            # 빈 DataFrame도 저장할 수 있도록 처리
            pd.DataFrame({'메시지': ['분석된 키워드가 없습니다.']}).to_excel(writer, index=False, sheet_name='키워드 분석 결과')

        # 추천 상품명 시트 저장
        if suggestions is not None and not suggestions.empty:
            suggestions.to_excel(writer, index=False, sheet_name='추천 상품명')
        else:
            pd.DataFrame({'메시지': ['추천 상품명이 없습니다.']}).to_excel(writer, index=False, sheet_name='추천 상품명')

    output.seek(0)
    return output.getvalue()