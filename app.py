import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names

st.set_page_config(page_title="상품명 최적화 도우미", layout="centered")

st.title("🛍️ 네이버 스마트스토어 상품명 자동 생성기")
st.markdown("분석할 키워드를 입력하면 검색량 기반으로 최적화된 상품명을 추천해드립니다.")

keyword = st.text_input("🔍 키워드를 입력하세요", "")

if st.button("분석 시작") and keyword.strip():
    with st.spinner("키워드 분석 중..."):
        df = analyze_keywords(keyword)

    if df.empty:
        st.warning("검색 결과가 없습니다. 다른 키워드를 입력해보세요.")
    else:
        st.subheader("📊 키워드 분석 결과")
        st.dataframe(df)

        st.subheader("🎯 추천 상품명 (가중치 기반 순위)")
        ranked = generate_weighted_ranked_product_names(df)
        st.dataframe(ranked)

        # 엑셀 다운로드
        st.download_button(
            label="📁 엑셀로 저장",
            data=df.to_excel(index=False, engine='openpyxl'),
            file_name="keyword_analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("키워드를 입력하고 버튼을 눌러주세요.")
