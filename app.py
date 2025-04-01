import streamlit as st
from keyword_analyzer import analyze_keywords
from weighted_product_name_generator import generate_weighted_ranked_product_names
from save_to_excel import save_analysis_and_suggestions_to_excel
from category_mapper import guess_category
from datetime import datetime

st.set_page_config(page_title="네이버 스마트스토어 상품명 생성기", layout="wide")
st.title("🛒 네이버 스마트스토어 상품명 최적화 도구")

main_keyword = st.text_input("🔍 분석할 메인 키워드를 입력하세요:")

if main_keyword:
    with st.spinner("분석 중입니다...⏳"):
        # 1. 키워드 분석 및 연관 키워드 추출
        df, related_keywords = analyze_keywords(main_keyword)

        if df is not None and not df.empty:
            # 2. 카테고리 추정
            category = guess_category(main_keyword)

            # 3. 상품명 추천
            suggestions = generate_weighted_ranked_product_names(df, main_keyword)

            # 4. 결과 출력
            st.subheader("📈 키워드 분석 결과")
            st.markdown("**✔️ 추출된 연관 키워드:**")
            st.write(", ".join(related_keywords))

            st.markdown("**📁 예측 카테고리:**")
            st.write(category)

            st.dataframe(df.style.format({
                "총 검색량": "{:.0f}",
                "광고 입찰가": "₩{:.0f}",
                "상품 수": "{:.0f}",
                "평균 가격": "₩{:.0f}",
                "종합 점수": "{:.2f}"
            }))

            st.subheader("📝 추천 상품명")
            for i, name in enumerate(suggestions[:10], 1):
                st.markdown(f"**{i}.** {name}")

            # 5. 결과 저장
            file_name = f"{main_keyword}_분석결과_{datetime.now().strftime('%Y%m%d')}.xlsx"
            excel_data = save_analysis_and_suggestions_to_excel(df, suggestions)

            st.download_button(
                "⬇️ 결과 Excel 다운로드",
                data=excel_data,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("❗ 키워드 분석 결과가 없습니다. 다른 키워드를 입력해보세요.")
