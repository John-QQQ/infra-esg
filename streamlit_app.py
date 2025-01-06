import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from transformers import pipeline

# 💡 뉴스 크롤링 함수
def get_naver_news(keywords, start_date, end_date):
    """네이버 뉴스에서 키워드 조합으로 최대 7개의 뉴스 기사 제목과 링크를 댓글 수, 발표 시간, 출처 정보와 함께 가져옵니다."""
    news_list = []
    
    for keyword in keywords:
        url = (
            f"https://search.naver.com/search.naver?where=news&query={keyword}"
            f"&pd=4&ds={start_date}&de={end_date}"
        )
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('.news_tit')  # 뉴스 제목 선택자
        
        # 뉴스 정보 수집
        for article in articles:
            title = article.get_text()
            link = article['href']
            comment_count = 0  # 댓글 수 초기화
            time = article.find_next('span', {'class': 'info'})  # 발표 시간
            source = article.find_next('a', {'class': 'info_nclicks'})  # 출처

            # 댓글 수 추출
            comment_section = article.find_next('a', {'class': 'nclicks(fls.comment)'})
            if comment_section:
                comment_count = int(comment_section.get_text().replace(',', ''))  # 숫자만 추출하여 정수형으로 변환
                
            if time:
                time = time.get_text()  # 기사 발표 시간
            else:
                time = '발표 시간 없음'

            if source:
                source = source.get_text()  # 뉴스 출처
            else:
                source = '출처 없음'
                
            # 뉴스 본문 요약 추가
            summary = get_news_summary(link)
            
            news_list.append((title, link, comment_count, time, source, summary))
            
            # 최대 7개의 뉴스만 가져오기
            if len(news_list) >= 7:
                break
        
        if len(news_list) >= 7:
            break

    # 댓글 수 기준으로 내림차순 정렬
    sorted_news = sorted(news_list, key=lambda x: x[2], reverse=True)[:7]
    return sorted_news

# 뉴스 본문을 두 가지 수준으로 요약하는 함수
def get_news_summary(link):
    """뉴스 본문을 가져와 요약합니다."""
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 뉴스 본문 추출 (네이버 뉴스의 본문은 'div'태그에 포함됨)
        content = soup.select_one('.newsct_article')  # 기사 본문
        if content:
            full_text = content.get_text().strip()
            
            # 요약 모델 로드 (첫 번째 요약: 간략한 요약)
            summarizer = pipeline("summarization")
            summary_short = summarizer(full_text[:1000], max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            
            # 두 번째 요약: 더 긴 요약
            summary_long = summarizer(full_text[:2000], max_length=300, min_length=100, do_sample=False)[0]['summary_text']
            
            return summary_short, summary_long
        else:
            return '본문을 찾을 수 없습니다.', '본문을 찾을 수 없습니다.'
    except Exception as e:
        return '요약 실패', '요약 실패'

# Streamlit App
st.title("ESG & Network Insights Weekly News")

# 1. ESG Trends Summary
with st.expander("금주의 ESG 트렌드 요약"):
    st.write("여기에 금주의 ESG 트렌드 요약 내용을 추가하세요.")

# 2. Global & Local News
with st.expander("국내외 주요 뉴스"):
    st.write("주요 키워드를 선택하세요 (최대 7개 뉴스 표시).")

    # 키워드 선택 (가로 배치)
    keywords = ["환경", "사회", "거버넌스", "기술", "경제", "정치", "글로벌 트렌드"]
    cols = st.columns(len(keywords))
    selected_keywords = [kw for i, kw in enumerate(keywords) if cols[i].checkbox(kw)]

    # 🔄 일주일 자동 필터 설정
    end_date = datetime.today()  # 오늘 날짜
    start_date = end_date - timedelta(days=7)  # 일주일 전 날짜

    st.write(f"뉴스 검색 기간: {start_date.strftime('%Y.%m.%d')} ~ {end_date.strftime('%Y.%m.%d')}")

    # 뉴스 크롤링 실행
    if st.button("뉴스 가져오기"):
        if selected_keywords:
            news = get_naver_news(selected_keywords, start_date.strftime('%Y.%m.%d'), end_date.strftime('%Y.%m.%d'))
            if news:
                st.write("### 검색된 뉴스 목록:")
                for title, link, comment_count, time, source, (summary_short, summary_long) in news:
                    st.write(f"**제목**: [{title}]({link})")
                    st.write(f"- **댓글 수**: {comment_count}")
                    st.write(f"- **발표 시간**: {time}")
                    st.write(f"- **출처**: {source}")
                    st.write(f"- **간략 요약**: {summary_short}")
                    st.write(f"- **자세한 요약**: {summary_long}")
                    st.write("---")
            else:
                st.write("해당 기간에 관련 뉴스가 없습니다.")
        else:
            st.write("키워드를 선택하세요.")

# 3. SKT Network Insights
with st.expander("인사이트 for SKT Network"):
    st.write("여기에 SKT Network 관련 인사이트 내용을 추가하세요.")

# Footer
st.markdown("**Weekly News Collection App** - ESG & Network Insights")
