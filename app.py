import streamlit as st
import pandas as pd
import datetime
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_to_excel

# ------------------- 테마 감지 (시간 기반) -------------------
now_hour = datetime.datetime.now().hour
is_dark = now_hour >= 18 or now_hour < 6

if is_dark:
    bg_color = "#1E1E1E"
    text_color = "#FFFFFF"
    accent_color = "#7FDBFF"
else:
    bg_color = "#FFFFFF"
    text_color = "#222222"
    accent_color = "#0077C8"

# ------------------- 페이지 설정 -------------------
st.set_page_config(
    page_title="스마트스토어 상품명 최적화",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ------------------- 스타일 커스텀 -------------------
st.markdown(f"""
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .main-title {{
            font-size: 2.3em;
            font-weight: bold;
            color: {accent_color};
            text-align: center;
            padding: 10px 0;
        }}
        .sub-header {{
            font-size: 1.1em;
            color: #888888;
            text-align: center;
            margin-bottom: 30px;
        }}
        .stButton > button {{
            background-color: {accent_color};
            color: white;
            border-radius: 8px;
            padding: 0.6em 1em;
            border: none;
        }}
        .stButton > button:hover {{
            background-color: #005B9E;
        }}
    </style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.markdown('<div class="main-title">🛒 스마트스토어 상품명 최적화 도우미</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">키워드 분석 + 경쟁 강도 기반 추천 상품명을 생성합니다.</div>', unsafe_allow_html=True)

# ------------------- INPUT -------------------
st.markdown("### 🔍 키워드 입력")
main_keyword = st.text_input("예: 무선 충전기, 감성 랜턴, 미니 선풍기 등")

# ------------------- 실행 버튼 -------------------
if st.button("📊 분석 시작") and main_keyword.strip():
    with st.spinner("📡 NAVER API에서 데이터를 불러오는 중입니다..."):
        df = analyze_keywords(main_keyword)

    if not df.empty:
        st.success("✅ 키워드 분석이 완료되었습니다!")

        # ------------------- 분석 결과 -------------------
        st.markdown("### 📈 키워드 분석 결과")
        st.dataframe(df.style.format({"월간 검색량(합산)": "{:,}"}), use_container_width=True)

        with st.spinner("🤖 상품명을 생성 중입니다..."):
            suggestions = generate_weighted_ranked_product_names(df)

        # ------------------- 추천 상품명 -------------------
        if suggestions:
            st.markdown("### 💡 추천 상품명")
            for i, name in enumerate(suggestions, 1):
                st.markdown(
                    f"<div style='font-size:1.1em; padding:4px 0;'>🔹 <b>{i}. {name}</b></div>",
                    unsafe_allow_html=True
                )

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