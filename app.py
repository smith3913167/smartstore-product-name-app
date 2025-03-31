import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_to_excel

st.set_page_config(
    page_title="스마트스토어 상품명 최적화 도우미",
    layout="centered"
)

st.title("🛍️ 네이버 스마트스토어 상품명 최적화 도우미")
st.markdown("🔍 키워드 기반 검색량, 경쟁 강도 분석을 통해 최적의 상품명을 추천합니다.")

# 1. 키워드 입력
main_keyword = st.text_input("분석할 키워드를 입력하세요 (예: 무선 충전기, 감성 랜턴 등)")

if st.button("🚀 키워드 분석 시작") and main_keyword.strip():
    with st.spinner("분석 중입니다..."):
        # 2. 키워드 분석
        df = analyze_keywords(main_keyword)

        # 3. 결과 시각화
        if not df.empty:
            st.success("✅ 키워드 분석 완료!")
            st.subheader("📊 키워드 분석 결과")
            st.dataframe(df, use_container_width=True)

            # 4. 추천 상품명 생성
            suggestions = generate_weighted_ranked_product_names(df)

            if suggestions:
                st.subheader("📌 추천 상품명 (가중치 기반)")
                for i, name in enumerate(suggestions, 1):
                    st.markdown(f"{i}. {name}")

                # 5. 다운로드 버튼
                excel_data = save_to_excel(df, suggestions)
                st.download_button(
                    label="📥 결과 다운로드 (Excel)",
                    data=excel_data,
                    file_name="keyword_analysis.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("❗ 추천할 상품명이 없습니다. 키워드를 다시 입력해 주세요.")
        else:
            st.error("❗ 키워드 분석 결과가 없습니다. 유효한 키워드를 입력해 주세요.")