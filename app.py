import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from io import BytesIO

# 웹 페이지 기본 설정
st.set_page_config(
    page_title="상품명 최적화 도우미",
    layout="centered",
    page_icon="🛍️"
)

st.title("🛍️ 네이버 스마트스토어 상품명 자동 생성기")
st.write("분석할 키워드를 입력하면 검색량 기반으로 최적화된 상품명을 추천해드립니다.")

# 키워드 입력 받기
keyword = st.text_input("🔍 키워드를 입력하세요", placeholder="예: 캠핑의자, 차량용선풍기 등")

# 분석 버튼
if st.button("분석 시작") and keyword:
    with st.spinner("키워드를 분석 중입니다..."):
        df = analyze_keywords(keyword)

        if df is not None and not df.empty:
            st.success("✅ 키워드 분석이 완료되었습니다.")
            st.dataframe(df, use_container_width=True)

            # 알고리즘 기반 추천 상품명 생성
            suggestions = generate_weighted_ranked_product_names(df)

            if suggestions:
                st.markdown("### 🧠 추천 상품명 (우선순위 순)")
                for i, name in enumerate(suggestions, 1):
                    st.write(f"{i}. {name}")

                # 📥 결과 다운로드 버튼
                st.markdown("---")
                buffer = BytesIO()
                df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)

                st.download_button(
                    label="📥 결과 Excel 다운로드",
                    data=buffer,
                    file_name="keyword_analysis.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("추천할 상품명이 없습니다. 키워드 데이터를 다시 확인해 주세요.")
        else:
            st.warning("검색 결과가 없습니다. 다른 키워드를 입력해보세요.")
