import streamlit as st
from keyword_analyzer import analyze_keywords
from category_mapper import guess_category
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_analysis_and_suggestions_to_excel
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="스마트스토어 상품명 추천기", layout="wide")

st.title("🛒 네이버 스마트스토어 상품명 자동 생성기")

main_keyword = st.text_input("🔍 분석할 메인 키워드 입력", "무선충전기")

if st.button("분석 시작") and main_keyword:
    with st.spinner("분석 중입니다...⏳"):
        try:
            df, related_keywords = analyze_keywords(main_keyword)
            category = guess_category(main_keyword)

            if df is not None and not df.empty:
                suggestions = generate_weighted_ranked_product_names(df, main_keyword)

                st.subheader("📈 키워드 분석 결과")
                st.dataframe(df)

                st.subheader("🔎 연관 키워드")
                st.write(", ".join(related_keywords))

                st.subheader("📦 예상 카테고리")
                st.write(f"🗂️ {category}")

                st.subheader("✨ 추천 상품명")
                st.table(suggestions)

                file_name = f"{main_keyword}_추천결과_{datetime.now().strftime('%Y%m%d')}.xlsx"
                if st.download_button("⬇️ 결과 Excel 다운로드", data=save_analysis_and_suggestions_to_excel(df, suggestions), file_name=file_name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
                    st.success("✅ 엑셀 파일 다운로드 완료!")

            else:
                st.warning("분석 결과가 없습니다. 키워드를 다시 입력해 주세요.")
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")