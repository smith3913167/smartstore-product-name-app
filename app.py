import streamlit as st
import pandas as pd

from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_analysis_and_suggestions_to_excel  # 있으면 포함

st.set_page_config(page_title="📦 스마트스토어 상품명 추천기", layout="wide")
st.title("📦 스마트스토어 상품명 최적화 도구")

# 1️⃣ 사용자 키워드 입력
main_keyword = st.text_input("분석할 메인 키워드를 입력하세요:", value="캠핑의자")

# 2️⃣ 분석 버튼
if st.button("🔍 키워드 분석 및 상품명 추천 시작"):
    if not main_keyword:
        st.warning("⛔ 키워드를 입력해주세요.")
    else:
        with st.spinner("🔍 분석 중입니다... 잠시만 기다려주세요."):
            df = analyze_keywords(main_keyword)

            if df is None or df.empty:
                st.error("❌ 분석 결과가 없습니다. 다른 키워드를 입력해보세요.")
            else:
                # 3️⃣ 추천 상품명 생성
                suggestions = generate_weighted_ranked_product_names(df, main_keyword)

                # 4️⃣ 키워드 분석 결과 표시
                st.subheader("📈 키워드 분석 결과")

                # 컬럼 자동 매핑용 rename dictionary
                display_df = df.rename(columns={
                    "총 검색량": "검색량",
                    "광고비": "광고비",
                    "평균가": "평균가"
                })

                try:
                    st.dataframe(
                        display_df.style
                        .format({
                            "검색량": "{:,}",
                            "광고비": "₩{:,}",
                            "평균가": "₩{:,}"
                        })
                        .highlight_max(subset=["검색량", "광고비", "평균가"], color="lightgreen"),
                        use_container_width=True
                    )
                except KeyError as e:
                    st.warning(f"⚠️ 시각화에 필요한 컬럼이 없습니다: {e}")

                # 5️⃣ 추천 상품명 출력
                st.subheader("🎯 추천 상품명 리스트")
                st.dataframe(suggestions, use_container_width=True)

                # 6️⃣ 다운로드 옵션
                st.markdown("---")
                file_name = f"{main_keyword}_분석결과.xlsx"
                if st.download_button("⬇️ 결과 Excel 다운로드", data=save_analysis_and_suggestions_to_excel(df, suggestions), file_name=file_name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
                    st.success("✅ 엑셀 다운로드가 완료되었습니다.")