import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_to_excel

# 페이지 설정
st.set_page_config(
    page_title="스마트스토어 상품명 최적화",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ------------------- HEADER -------------------
st.markdown("""
    <style>
        .main-title {
            font-size: 2.2em;
            font-weight: bold;
            color: #262730;
            text-align: center;
            padding: 10px 0;
        }
        .sub-header {
            font-size: 1.2em;
            color: #555;
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛒 스마트스토어 상품명 최적화 도우미</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">키워드 분석 + 경쟁 강도 기반 추천 상품명을 생성합니다.</div>', unsafe_allow_html=True)

# ------------------- INPUT -------------------
st.markdown("### 🔍 키워드 입력")
main_keyword = st.text_input("예: 무선 충전기, 감성 랜턴, 미니 선풍기 등")

# ------------------- 실행 버튼 -------------------
if st.button("📊 분석 시작") and main_keyword.strip():
    with st.spinner("분석 중입니다..."):
        df = analyze_keywords(main_keyword)

        if not df.empty:
            st.success("✅ 키워드 분석이 완료되었습니다!")

            # ------------------- 분석 결과 -------------------
            st.markdown("### 📈 키워드 분석 결과")
            st.dataframe(df.style.format({"월간 검색량(합산)": "{:,}"}), use_container_width=True)

            # ------------------- 추천 상품명 -------------------
            suggestions = generate_weighted_ranked_product_names(df)

            if suggestions:
                st.markdown("### 💡 추천 상품명")
                for i, name in enumerate(suggestions, 1):
                    st.markdown(f"<div style='font-size:1.1em; padding:4px 0;'>🔹 <b>{i}. {name}</b></div>", unsafe_allow_html=True)

                # ------------------- 다운로드 -------------------
                st.markdown("---")
                excel_file = save_to_excel(df, suggestions)
                st.download_button(
                    label="📥 Excel로 저장하기",
                    data=excel_file,
                    file_name="상품명_키워드분석.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("⚠️ 유효한 추천 상품명이 생성되지 않았습니다.")
        else:
            st.error("❗ 분석 결과가 없습니다. 다른 키워드를 입력해 보세요.")