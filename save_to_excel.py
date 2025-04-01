import pandas as pd
from io import BytesIO

def save_analysis_and_suggestions_to_excel(df_analysis, suggestions):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # 키워드 분석 결과 저장
        df_analysis.to_excel(writer, index=False, sheet_name="키워드 분석")

        # 추천 상품명 저장
        if suggestions:
            df_suggestions = pd.DataFrame(suggestions)
            df_suggestions.to_excel(writer, index=False, sheet_name="추천 상품명")

    output.seek(0)
    return output