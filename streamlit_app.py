import streamlit as st

# App Title
st.title("ESG & Network Insights Weekly News")

# 1. ESG Trends Summary
with st.expander("금주의 ESG 트렌드 요약"):
    st.write("여기에 금주의 ESG 트렌드 요약 내용을 추가하세요.")
    # ESG 트렌드 관련 데이터나 요약 등을 추가할 수 있습니다.

# 2. Global & Local News
with st.expander("국내외 주요 뉴스"):
    # 키워드 선택 (체크박스를 가로로 배치)
    st.write("주요 키워드를 선택하세요 (중복 선택 가능):")
    keywords = ["환경", "사회", "거버넌스", "기술", "경제", "정치", "글로벌 트렌드"]

    # 가로로 배치할 열 개수 설정
    cols = st.columns(4)  # 4개의 열을 생성 (필요에 따라 조정 가능)

    selected_keywords = []
    for i, keyword in enumerate(keywords):
        if cols[i % 4].checkbox(keyword):  # 각 열에 체크박스를 배치
            selected_keywords.append(keyword)

    # 국내, 해외 뉴스를 가로로 배치
    col1, col2 = st.columns(2)

    # 국내 뉴스
    with col1:
        st.header("국내 주요 뉴스")
        st.write("선택된 키워드에 맞는 국내 주요 뉴스를 표시합니다.")
        st.write(f"선택된 키워드: {', '.join(selected_keywords)}")
        # 선택된 키워드에 맞는 뉴스 필터링 로직 추가
        # 예시: 각 키워드에 대해 필터링된 뉴스 제공

    # 해외 뉴스
    with col2:
        st.header("해외 주요 뉴스")
        st.write("선택된 키워드에 맞는 해외 주요 뉴스를 표시합니다.")
        st.write(f"선택된 키워드: {', '.join(selected_keywords)}")
        # 선택된 키워드에 맞는 뉴스 필터링 로직 추가
        # 예시: 각 키워드에 대해 필터링된 뉴스 제공

# 3. SKT Network Insights
with st.expander("인사이트 for SKT Network"):
    st.write("여기에 SKT Network 관련 인사이트 내용을 추가하세요.")
    # SKT Network 관련 최신 동향이나 분석 정보를 추가할 수 있습니다.

# Footer or additional features
st.markdown("**Weekly News Collection App** - ESG & Network Insights")
