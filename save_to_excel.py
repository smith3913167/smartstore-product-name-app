import pandas as pd
from io import BytesIO

def save_to_excel(df, suggestions):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # 키워드 분석 데이터 저장
        df.to_excel(writer, index=False, sheet_name="키워드 분석")

        # 추천 상품명 저장
        if suggestions:
            suggestion_df = pd.DataFrame({"추천 상품명": suggestions})
            suggestion_df.to_excel(writer, index=False, sheet_name="추천 상품명")

    output.seek(0)
    return output