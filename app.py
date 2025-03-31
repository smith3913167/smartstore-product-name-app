# app.py
import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_analysis_and_suggestions_to_excel
from datetime import datetime

st.set_page_config(
    page_title="스마트스토어 상품명 최적화 도우미",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
    <style>
    body {
        font-family: 'Noto Sans KR', sans-serif;
    }
    .stDataFrame thead tr th {
        background-color: #f0f2f6;
        color: black;
        text-align: center;
    }
    .reportview-container .main footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🛒 스마트스토어 상품명 최적화 도우미")
st.write("키워드 분석 + 경쟁 강도 기반 추천 상품명을 생성합니다.")

keyword = st.text_input("🔍 키워드 입력", placeholder="예: 무선 충전기, 감성 랜턴, 미니 선풍기 등")

if st.button("📊 분석 시작"):
    if keyword:
        with st.spinner("키워드 분석 중입니다..."):
            df = analyze_keywords(keyword)
            suggestions = generate_weighted_ranked_product_names(df)
            excel_data = save_analysis_and_suggestions_to_excel(df, suggestions)

        st.success("✅ 키워드 분석이 완료되었습니다!")

        st.subheader("📈 키워드 분석 결과")
        st.dataframe(df.style.format({
            '월간 검색량': '{:,}',
            '광고비': '{:,}',
            '상품수': '{:,}',
            '평균가': '{:,}원'
        }))

        if suggestions:
            st.subheader("💡 추천 상품명")
            for i, name in enumerate(suggestions, 1):
                st.markdown(f"🔹 **{i}. {name}**")
        else:
            st.warning("추천할 상품명이 없습니다. 키워드 데이터를 다시 확인해 주세요.")

        st.download_button(
            label="📥 Excel로 저장하기",
            data=excel_data,
            file_name=f"keyword_analysis_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("분석할 키워드를 입력해 주세요.")

