import import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_results_to_excel

st.set_page_config(
    page_title="네이버 스마트스토어 상품명 자동 생성기",
    layout="centered"
)

st.markdown("""
    <h1>🛍️ 네이버 스마트스토어 상품명 자동 생성기</h1>
    <p>분석할 키워드를 입력하면 검색량 기반으로 최적화된 상품명을 추천해드립니다.</p>
""", unsafe_allow_html=True)

main_keyword = st.text_input("🔍 키워드를 입력하세요", placeholder="예: 무선충전기")

if st.button("분석 시작"):
    if not main_keyword.strip():
        st.warning("키워드를 입력해주세요.")
    else:
        df = analyze_keywords(main_keyword)

        if df.empty:
            st.warning("검색 결과가 없습니다. 다른 키워드를 입력해보세요.")
        else:
            st.success("✅ 키워드 분석이 완료되었습니다.")
            st.dataframe(df)

            suggestions = generate_weighted_ranked_product_names(main_keyword, df)

            if not suggestions:
                st.warning("추천할 상품명이 없습니다. 키워드 데이터를 다시 확인해 주세요.")
            else:
                st.subheader("✨ 추천 상품명 (우선순위 순)")
                for i, name in enumerate(suggestions, 1):
                    st.markdown(f"**{i}. {name}**")

                # 엑셀 저장
                save_results_to_excel(df, suggestions)
                with open("keyword_analysis.xlsx", "rb") as f:
                    st.download_button(
                        label="📁 결과 엑셀 다운로드",
                        data=f,
                        file_name="keyword_analysis.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

