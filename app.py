import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_analysis_and_suggestions_to_excel

# ✅ 페이지 설정
st.set_page_config(
    page_title="스마트스토어 상품명 추천 도우미",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ 테마 설정 (낮/밤 시간 자동 감지 테마)
from datetime import datetime
hour = datetime.now().hour
theme = "dark" if hour < 7 or hour >= 18 else "light"
st.markdown(f"<style>body {{ background-color: {'#0E1117' if theme == 'dark' else '#FFFFFF'}; color: {'#FAFAFA' if theme == 'dark' else '#000000'} }}</style>", unsafe_allow_html=True)

# ✅ 타이틀 영역
st.title("🔍 네이버 스마트스토어 상품명 추천 시스템")
st.caption("PandaRank 스타일 키워드 분석 기반 · 광고비/검색량/경쟁강도 반영 · 자동 상품명 생성 · Excel 저장")

# ✅ 메인 키워드 입력
main_keyword = st.text_input("분석할 메인 키워드를 입력하세요:", placeholder="예: 무선충전기")

# ✅ 분석 실행
if st.button("📊 키워드 분석 및 상품명 추천 시작") and main_keyword:
    with st.spinner("분석 중입니다...⏳"):

        # 1. 키워드 분석
        df = analyze_keywords(main_keyword)

        if df is not None and not df.empty:
            # 2. 상품명 추천
            suggestions = generate_weighted_ranked_product_names(df, main_keyword)

            # 3. 결과 출력
            st.subheader("📈 키워드 분석 결과")
            st.dataframe(
                df.style
                .format({"검색량": "{:.0f}", "광고비": "₩{:.0f}", "평균가": "₩{:.0f}"})
                .highlight_max(color="#ffd166", subset=["검색량", "광고비", "평균가"])
                .highlight_min(color="#06d6a0", subset=["경쟁 점수"])
                .set_properties(**{"text-align": "center"}),
                use_container_width=True
            )

            st.subheader("💡 추천 상품명 (상위 5개)")
            for i, row in suggestions.head(5).iterrows():
                st.markdown(f"**{i+1}. {row['추천 상품명']}**")

            # 4. 다운로드
            excel_file = save_analysis_and_suggestions_to_excel(df, suggestions)

            st.download_button(
                label="📥 엑셀 파일 다운로드",
                data=excel_file,
                file_name=f"{main_keyword}_키워드_분석결과.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("분석 결과가 없습니다. 키워드를 다시 확인해보세요.")