import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_analysis_and_suggestions_to_excel

st.set_page_config(page_title="네이버 스마트스토어 상품명 자동 생성기", layout="centered")

st.title("🛍️ 네이버 스마트스토어 상품명 자동 생성기")
st.write("분석할 키워드를 입력하면 검색량 기반으로 최적화된 상품명을 추천해드립니다.")

keyword = st.text_input("🔍 키워드를 입력하세요", placeholder="예: 무선청소기")

if st.button("분석 시작"):
    if not keyword.strip():
        st.warning("키워드를 입력해주세요.")
    else:
        with st.spinner("키워드를 분석 중입니다..."):
            df = analyze_keywords(keyword)

        if df is not None and not df.empty:
            st.success("✅ 키워드 분석이 완료되었습니다.")
            st.dataframe(df.style.format({'월간 검색량(합산)': '{:.0f}'}), use_container_width=True)

            with st.spinner("추천 상품명을 생성 중입니다..."):
                suggestions = generate_weighted_ranked_product_names(keyword, df)

            if suggestions:
                st.subheader("📢 추천 상품명 (가중치 기반 상위 5개)")
                for i, name in enumerate(suggestions, 1):
                    st.markdown(f"**{i}.** {name}")

                # Excel 저장
                save_analysis_and_suggestions_to_excel(df, suggestions)
                with open("keyword_analysis.xlsx", "rb") as file:
                    st.download_button(
                        label="📥 결과 Excel 다운로드",
                        data=file,
                        file_name="keyword_analysis.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.warning("추천할 상품명이 없습니다. 키워드 데이터를 다시 확인해 주세요.")
        else:
            st.error("❌ 키워드 분석 결과가 없습니다. 다른 키워드로 시도해 주세요.")
