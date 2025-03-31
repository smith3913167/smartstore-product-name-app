import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_to_excel

st.set_page_config(page_title="📦 스마트스토어 상품명 최적화기", layout="centered")

st.title("📦 네이버 스마트스토어 상품명 자동 생성기")
st.markdown("⛺ 키워드를 입력하면 연관 키워드 분석과 검색량·경쟁도 기반으로 최적의 상품명을 추천해드립니다.")

# 🔍 사용자 입력
main_keyword = st.text_input("📝 분석할 대표 키워드를 입력하세요 (예: 휴대용 선풍기)", max_chars=50)

if main_keyword:
    with st.spinner("🔍 키워드 분석 중..."):
        df = analyze_keywords(main_keyword)

    st.success("✅ 키워드 분석 완료!")
    st.dataframe(df)

    # 🔧 가중치 기반 상품명 생성
    with st.spinner("🤖 스마트 추천 상품명 생성 중..."):
        suggestions = generate_weighted_ranked_product_names(df)

    if not suggestions.empty:
        st.markdown("### 🔝 추천 상품명 (가중치 기반)")
        st.dataframe(suggestions)

        # 📁 엑셀 다운로드 버튼
        excel_data = save_to_excel(df, suggestions["상품명"].tolist())
        st.download_button(
            label="📥 분석결과 + 추천상품명 엑셀 다운로드",
            data=excel_data,
            file_name="keyword_analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ 유효한 추천 상품명이 생성되지 않았습니다.")
