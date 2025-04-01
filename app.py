import streamlit as st
import pandas as pd
from keyword_analyzer import analyze_keyword
from weighted_product_name_generator import generate_weighted_ranked_product_names

st.set_page_config(page_title="스마트스토어 상품명 추천 시스템", layout="wide")

st.title("🔍 네이버 스마트스토어 상품명 추천 시스템")
st.markdown("""
PandaRank 스타일 키워드 분석 기반 · 광고비/검색량/경쟁강도 반영 · 자동 상품명 생성 · Excel 저장
""")

main_keyword = st.text_input("분석할 메인 키워드를 입력하세요:", "보조배터리")

if st.button("📊 키워드 분석 및 상품명 추천 시작"):
    with st.spinner("키워드 분석 및 추천 상품명 생성 중..."):
        try:
            # 1. 키워드 분석
            df = analyze_keyword(main_keyword)

            if df is not None and not df.empty:
                # 2. 상품명 추천
                suggestions = generate_weighted_ranked_product_names(df, main_keyword)

                # ✅ 자동 컬럼 매핑 기준 설정
                desired_columns_map = {
                    "검색량": ["검색량", "총 검색량", "PC 검색량+모바일 검색량"],
                    "광고비": ["광고비", "광고 입찰가", "광고비용"],
                    "평균가": ["평균가", "평균 가격", "평균단가"]
                }

                # ✅ 실제 컬럼명으로 자동 매핑
                available_columns = df.columns.tolist()
                resolved_columns = {}
                for key, candidates in desired_columns_map.items():
                    for candidate in candidates:
                        if candidate in available_columns:
                            resolved_columns[key] = candidate
                            break

                # ✅ 스타일 적용할 컬럼 필터링
                highlight_targets = [resolved_columns.get("검색량"),
                                     resolved_columns.get("광고비"),
                                     resolved_columns.get("평균가")]
                highlight_targets = [col for col in highlight_targets if col]

                # 3. 분석 결과 출력
                st.subheader("📈 키워드 분석 결과")
                st.dataframe(
                    df.style
                    .format({
                        resolved_columns.get("검색량", "검색량"): "{:.0f}",
                        resolved_columns.get("광고비", "광고비"): "₩{:.0f}",
                        resolved_columns.get("평균가", "평균가"): "₩{:.0f}",
                        "종합 점수": "{:.2f}" if "종합 점수" in df.columns else "{:}"
                    })
                    .highlight_max(color="#ffd166", subset=highlight_targets)
                )

                # 4. 추천 상품명 출력
                st.subheader("📝 추천 상품명 리스트")
                for i, name in enumerate(suggestions, 1):
                    st.markdown(f"**{i}. {name}**")

                # 5. 다운로드
                st.download_button(
                    label="📥 엑셀 파일로 저장",
                    data=df.to_excel(index=False),
                    file_name=f"{main_keyword}_키워드분석결과.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("분석 결과가 없습니다. 키워드를 다시 확인해보세요.")
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")