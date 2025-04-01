import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_to_excel

# ✅ 페이지 설정
st.set_page_config(page_title="스마트스토어 상품명 최적화 도우미", layout="wide")

# ✅ 사용자 정의 스타일
st.markdown("""
    <style>
    .main { font-family: 'Pretendard', sans-serif; }
    div[data-testid="stSidebar"] { background-color: #f8f9fa; }
    </style>
""", unsafe_allow_html=True)

# ✅ 앱 제목
st.title("🛒 스마트스토어 상품명 최적화 도우미")
st.markdown("키워드 분석 + 경쟁 강도 기반 추천 상품명을 생성합니다.")

# ✅ 사용자 입력
keyword = st.text_input("🔍 키워드 입력", placeholder="예: 무선 충전기, 감성 랜턴, 미니 선풍기 등")

# ✅ 분석 시작 버튼
if st.button("📊 분석 시작") and keyword:
    with st.spinner("키워드 데이터를 분석 중입니다..."):

        try:
            # 1. 키워드 분석
            df = analyze_keywords(keyword)

            if df.empty:
                st.warning("❗ 유효한 키워드 데이터를 찾을 수 없습니다.")
            else:
                st.success("✅ 키워드 분석이 완료되었습니다!")
                st.subheader("📈 키워드 분석 결과")
                st.dataframe(df.style.format({"월간 검색량": "{:,}", "상품수": "{:,}", "평균가": "{:,}원"}), use_container_width=True)

                # 2. 추천 상품명 생성
                suggestions = generate_weighted_ranked_product_names(df)

                st.subheader("💡 추천 상품명")
                if suggestions:
                    for i, name in enumerate(suggestions, 1):
                        st.markdown(f"🔹 **{i}. {name}**")
                else:
                    st.info("추천할 상품명이 없습니다. 키워드 데이터를 다시 확인해 주세요.")

                # 3. 엑셀 저장
                st.markdown("---")
                excel_data = save_to_excel(df, suggestions)
                st.download_button(
                    label="📥 Excel로 저장하기",
                    data=excel_data,
                    file_name=f"{keyword}_분석결과.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except Exception as e:
            st.error(f"❌ 앱 실행 중 오류 발생: {e}")

# 기본 설명 출력
elif not keyword:
    st.info("좌측 상단 입력창에 키워드를 입력 후 [분석 시작] 버튼을 눌러주세요.")