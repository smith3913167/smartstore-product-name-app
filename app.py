import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_to_excel

# 페이지 설정
st.set_page_config(page_title="스마트스토어 상품명 최적화 도우미", layout="wide")

# 타이틀 및 설명
st.title("📦 스마트스토어 상품명 최적화 도우미")
st.markdown("네이버 연관 키워드를 분석하고 경쟁강도, 광고비, 상품 수 등을 고려하여 최적의 상품명을 추천합니다.")

# 사용자 입력
keyword = st.text_input("분석할 메인 키워드를 입력하세요:", placeholder="예: 무선충전기")

if keyword:
    with st.spinner("🔍 키워드 데이터를 분석 중입니다..."):
        df = analyze_keywords(keyword)
        st.success("✅ 키워드 분석 완료!")

        st.markdown("### 🔎 키워드 분석 결과")
        st.dataframe(df.style.highlight_max(axis=0, color="lightgreen"), use_container_width=True)

        # 상품명 추천
        with st.spinner("📈 상품명을 최적화 중입니다..."):
            suggestions = generate_weighted_ranked_product_names(df)

        if suggestions:
            st.markdown("### 📝 추천 상품명 Top 10")
            for i, name in enumerate(suggestions, 1):
                st.markdown(f"{i}. {name}")

            # 엑셀 저장
            buffer = save_to_excel(df, suggestions)
            st.download_button(
                label="📥 분석 결과 다운로드 (Excel)",
                data=buffer,
                file_name=f"{keyword}_분석결과.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("⚠️ 추천할 상품명이 없습니다. 데이터가 부족하거나 분석이 실패했을 수 있습니다.")