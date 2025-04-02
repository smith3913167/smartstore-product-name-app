import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from keyword_analyzer import analyze_keywords
from category_mapper import map_keyword_to_categories
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_analysis_and_suggestions_to_excel

st.set_page_config(page_title="스마트스토어 상품명 자동 생성기", layout="wide")
st.title("🛒 네이버 스마트스토어 상품명 자동 생성기")
st.caption("🔍 분석할 메인 키워드 입력")

main_keyword = st.text_input("분석할 메인 키워드를 입력하세요", placeholder="예: 보조배터리")

if st.button("분석 시작") and main_keyword:
    df, related_keywords = analyze_keywords(main_keyword)

    if df is not None and not df.empty:
        st.subheader("📈 키워드 분석 결과")
        st.dataframe(df)

        st.subheader("📊 연관 키워드 검색량 시각화")
        top_keywords = df.sort_values("검색량", ascending=False).head(10)
        plt.figure(figsize=(10, 5))
        sns.barplot(x="검색량", y="키워드", data=top_keywords, palette="viridis")
        st.pyplot(plt)

        st.subheader("📂 카테고리 분석 결과")
        categories = map_keyword_to_categories(main_keyword, related_keywords)
        if categories:
            cat_series = pd.Series(categories).value_counts()
            st.bar_chart(cat_series)

        st.subheader("📝 상품명 추천 결과")
        suggestions = generate_weighted_ranked_product_names(df, main_keyword)
        st.dataframe(suggestions)

        file_name = f"{main_keyword}_상품명_분석결과.xlsx"
        excel_data = save_analysis_and_suggestions_to_excel(df, suggestions)

        st.download_button(
            label="⬇️ 결과 Excel 다운로드",
            data=excel_data,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("분석 결과가 없습니다. 키워드를 다시 입력해 주세요.")
