import streamlit as st
from keyword_analyzer import analyze_keywords_pandarank_style
from weighted_product_name_generator import generate_weighted_product_names
from save_to_excel import save_analysis_and_suggestions

st.set_page_config(page_title="스마트스토어 키워드 분석기", layout="centered")

with st.sidebar:
    st.markdown("## 옵션")
    night_mode = st.checkbox("야간 모드")
    st.markdown("검색량 기준 추천 키워드 자동 생성")

st.markdown(f"""
    <style>
        body {{
            background-color: {'#1e1e1e' if night_mode else 'white'};
            color: {'white' if night_mode else 'black'};
        }}
        .stButton button {{
            background-color: {'#444' if night_mode else '#06f'};
            color: white;
        }}
    </style>
""", unsafe_allow_html=True)

st.title("🔍 네이버 스마트스토어 키워드 분석기")

user_input = st.text_input("분석할 키워드를 입력하세요 (쉼표로 구분)", "무선마우스, 게이밍마우스")
if st.button("분석 시작"):
    with st.spinner("분석 중입니다..."):
        keyword_list = [k.strip() for k in user_input.split(",") if k.strip()]
        df = analyze_keywords_pandarank_style(keyword_list)
        suggestions, scored_df = generate_weighted_product_names(df)
        excel_data = save_analysis_and_suggestions(scored_df, suggestions)

    st.success("분석이 완료되었습니다!")
    st.dataframe(scored_df.style.background_gradient(axis=0, cmap="BuGn"))

    st.markdown("### 추천 상품명")
    for i, name in enumerate(suggestions, 1):
        st.markdown(f"**{i}. {name}**")

    st.download_button(
        label="엑셀 파일 다운로드",
        data=excel_data,
        file_name="keyword_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
