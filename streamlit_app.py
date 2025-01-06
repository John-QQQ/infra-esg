import streamlit as st
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# 네이버 뉴스 크롤링 함수 (국내)
def fetch_local_news(keyword):
    url = f"https://search.naver.com/search.naver?&where=news&query={keyword}&sm=tab_opt"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_items = []
    
    for item in soup.select('.list_news > li'):
        title = item.select_one('.news_tit').text
        link = item.select_one('.news_tit')['href']
        source = item.select_one('.info_group .press').text if item.select_one('.info_group .press') else '출처 없음'
        date = item.select_one('.info_group .date').text if item.select_one('.info_group .date') else '날짜 없음'
        
        news_items.append({
            'title': title,
            'link': link,
            'source': source,
            'date': date,
        })

        # 최대 5개 뉴스만 반환
        if len(news_items) >= 5:
            break
    
    return news_items

# NewsAPI를 통한 해외 뉴스 크롤링 함수 (해외)
def fetch_international_news(keywords):
    api_key = 'YOUR_NEWSAPI_KEY'  # 발급받은 NewsAPI 키를 여기에 입력하세요.
    # 키워드를 영어로 변환
    translator = Translator()
    translated_keyword = translator.translate(keywords, src='ko', dest='en').text
    url = f"https://newsapi.org/v2/everything?q={translated_keyword}&language=en&sortBy=publishedAt&pageSize=5&apiKey={api_key}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return []

    news_data = response.json()
    
    news_items = []
    for article in news_data['articles']:
        news_items.append({
            'title': article['title'],
            'link': article['url'],
            'source': article['source']['name'],
            'date': article['publishedAt']
        })

        # 최대 5개 뉴스만 반환
        if len(news_items) >= 5:
            break
    
    return news_items

# 뉴스 중요도 계산 함수
def calculate_news_importance(news, selected_keywords):
    """
    뉴스 제목에 포함된 키워드의 개수를 세어서 중요도를 반환.
    중요도가 높을수록 뉴스가 위로 오게 됩니다.
    """
    importance = sum(1 for keyword in selected_keywords if keyword in news['title'])
    return importance

# Streamlit 앱
st.title("ESG & Network Insights Weekly News")

# 1. ESG Trends Summary
with st.expander("금주의 ESG 트렌드 요약"):
    st.write("여기에 금주의 ESG 트렌드 요약 내용을 추가하세요.")

# 2. Global & Local News
with st.expander("국내외 주요 뉴스"):
    # 키워드 선택 (체크박스를 가로로 배치)
    st.write("주요 키워드를 선택하세요 (중복 선택 가능):")
    keywords = ["환경", "사회", "거버넌스", "기술", "경제", "정치", "글로벌 트렌드", "ESG"]

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
        
        all_news = []
        for keyword in selected_keywords:
            st.write(f"**{keyword}** 키워드에 대한 뉴스 크롤링 중...")
            news_data = fetch_local_news(keyword)
            
            if news_data:
                for news in news_data:
                    all_news.append(news)
            
        # 뉴스 중요도 계산하여 정렬
        all_news = sorted(all_news, key=lambda x: calculate_news_importance(x, selected_keywords), reverse=True)

        # 최대 7개의 뉴스만 표시
        for i, news in enumerate(all_news[:7]):
            st.write(f"**{news['title']}** - {news['date']} (출처: {news['source']})")
            st.write(f"[기사 링크]({news['link']})")
            st.write("---")
        
        if not all_news:
            st.write("뉴스를 가져오지 못했습니다.")

    # 해외 뉴스
    with col2:
        st.header("해외 주요 뉴스")
        st.write("선택된 키워드에 맞는 해외 주요 뉴스를 표시합니다.")
        
        all_news = []
        for keyword in selected_keywords:
            st.write(f"**{keyword}** 키워드에 대한 뉴스 크롤링 중...")
            news_data = fetch_international_news(keyword)
            
            if news_data:
                for news in news_data:
                    all_news.append(news)
        
        # 뉴스 중요도 계산하여 정렬
        all_news = sorted(all_news, key=lambda x: calculate_news_importance(x, selected_keywords), reverse=True)

        # 최대 7개의 뉴스만 표시
        for i, news in enumerate(all_news[:7]):
            st.write(f"**{news['title']}** - {news['date']} (출처: {news['source']})")
            st.write(f"[기사 링크]({news['link']})")
            st.write("---")
        
        if not all_news:
            st.write("뉴스를 가져오지 못했습니다.")

# 3. SKT Network Insights
with st.expander("인사이트 for SKT Network"):
    st.write("여기에 SKT Network 관련 인사이트 내용을 추가하세요.")
    
# Footer or additional features
st.markdown("**Weekly News Collection App** - ESG & Network Insights")
