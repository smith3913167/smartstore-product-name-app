import pandas as pd
from io import BytesIO

def save_to_excel(df, suggestions):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="키워드 분석")
        if suggestions:
            pd.DataFrame({"추천 상품명": suggestions}).to_excel(writer, index=False, sheet_name="추천 상품명")
    output.seek(0)
    return output