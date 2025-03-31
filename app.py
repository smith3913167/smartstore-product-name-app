import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_to_excel

st.set_page_config(
    page_title="스마트스토어 상품명 최적화",
    layout="wide",
    page_icon="🛒"
)

# 테마 적용 (낮/밤 모드)
current_hour = pd.Timestamp.now().hour
if 6 <= current_hour < 18:
    theme = "light"
else:
    theme = "dark"

# 제목 및 설명
st.markdown(
    f"<h1 style='text-align:center;'>🛍️ 네이버 스마트스토어 상품명 최적화 도우미</h1>",
    unsafe_allow_html=True
)

st.markdown("**🔍 키워드를 입력하면 연관 키워드를 분석하고, 경쟁강도 및 광고비 등을 기반으로 최적의 상품명을 추천해드립니다.**")

# 사용자 입력
keyword = st.text_input("🎯 분석할 메인 키워드를 입력하세요", placeholder="예: 무선충전기")

if keyword:
    with st.spinner("데이터 분석 중입니다..."):
        df = analyze_keywords(keyword)
        if not df.empty:
            suggestions = generate_weighted_ranked_product_names(df)

            # 키워드 분석 결과 표시
            st.subheader("📊 키워드 분석 결과")
            styled_df = df.style.background_gradient(cmap='YlGnBu', subset=["검색량", "광고비", "상품수", "평균가"])\
                                 .bar(subset=["경쟁강도점수", "가중치점수"], color='#5cb85c')\
                                 .format(precision=2)
            st.dataframe(styled_df, use_container_width=True)

            # 추천 상품명 표시
            if not suggestions.empty:
                st.subheader("✨ 추천 상품명 (경쟁강도/검색량 가중치 기반)")
                for i, name in enumerate(suggestions["추천 상품명"], start=1):
                    st.markdown(f"**{i}.** {name}")

            # 엑셀 다운로드
            excel_data = save_to_excel(df, suggestions)
            st.download_button(
                label="📥 분석 결과 엑셀 다운로드",
                data=excel_data,
                file_name=f"{keyword}_분석결과.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("📭 유효한 데이터를 찾을 수 없습니다.")

