import re

app_code = """import os
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import streamlit as st
import pypdf
import google.generativeai as genai
import plotly.graph_objects as go
from bs4 import BeautifulSoup

# 1. 페이지 설정
st.set_page_config(
    page_title="Universal AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS 스타일 설정
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #3B82F6;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1.15rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 25px;
    }
    .sentiment-positive {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .sentiment-negative {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .sentiment-neutral {
        background-color: #F3F4F6;
        color: #374151;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 3. API Key 로드 자동화 (보안 우수)
gemini_key = ""
is_key_configured = False

try:
    if "GEMINI_API_KEY" in st.secrets:
        gemini_key = st.secrets["GEMINI_API_KEY"]
        is_key_configured = True
except Exception:
    pass

if not is_key_configured and os.environ.get("GEMINI_API_KEY"):
    gemini_key = os.environ.get("GEMINI_API_KEY")
    is_key_configured = True

# 4. 사이드바 UI 설정
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6165/6165584.png", width=80)
    st.markdown("### ⚙️ 설정 & API 키")
    
    if is_key_configured:
        st.success("🔒 API Key가 시스템 설정을 통해 연결되었습니다. (키 입력 생략 가능)")
    else:
        if "gemini_key" not in st.session_state:
            st.session_state.gemini_key = ""
            
        gemini_key_input = st.text_input(
            "Gemini API Key 입력:", 
            type="password", 
            value=st.session_state.gemini_key
        )
        if gemini_key_input:
            gemini_key = gemini_key_input
            st.session_state.gemini_key = gemini_key_input
            
    st.markdown("---")
    st.markdown("""
    **💡 기능 안내:**
    * **문서 & 링크 튜터 (RAG)**: PDF나 웹 URL의 글을 파싱하여 AI와 질의응답을 나누고 요약/퀴즈를 생성합니다.
    * **실시간 뉴스 감성 분석**: 검색한 키워드의 최신 뉴스 여론을 수집하여 감성 분포를 진단합니다.
    """)

# 5. Gemini 모델 글로벌 초기화
model = None
if gemini_key:
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Gemini API 설정 중 오류 발생: {e}")

# 메인 타이틀 렌더링
st.markdown("<div class='main-title'>🤖 Universal AI Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>데이터 분석 및 RAG 기반 AI 학습 보조 웹 애플리케이션</div>", unsafe_allow_html=True)

# 탭 구성
tab_tutor, tab_sentiment = st.tabs(["📚 문서 & 링크 튜터 (RAG)", "📊 실시간 뉴스 감성 분석"])

# ------------------------------------------------------------------
# RAG 유틸리티 함수
# ------------------------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_text_from_url(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
        element.decompose()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return '\n'.join(chunk for chunk in chunks if chunk)

def split_into_chunks(text, chunk_size=800, overlap=150):
    text = re.sub(r'\s+', ' ', text)
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def find_relevant_chunks(query, chunks, top_n=3):
    query_words = set(re.findall(r'\w+', query.lower()))
    if not query_words:
        return chunks[:top_n]
    scored_chunks = []
    for chunk in chunks:
        chunk_words = set(re.findall(r'\w+', chunk.lower()))
        overlap = len(query_words.intersection(chunk_words))
        scored_chunks.append((overlap, chunk))
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [chunk for score, chunk in scored_chunks[:top_n]]

# ------------------------------------------------------------------
# 탭 1: 문서 & 링크 튜터 (RAG)
# ------------------------------------------------------------------
with tab_tutor:
    st.markdown("### 📂 PDF 파일 또는 웹사이트 링크(URL) 분석")
    input_mode = st.radio("분석 방식을 선택하세요:", ["PDF 파일 업로드", "웹사이트 URL 입력"], horizontal=True, key="tutor_input_mode")

    raw_text = None
    source_name = None

    if input_mode == "PDF 파일 업로드":
        uploaded_file = st.file_uploader("PDF 파일을 선택하세요", type=["pdf"])
        if uploaded_file:
            source_name = uploaded_file.name
            if "source_name" not in st.session_state or st.session_state.source_name != source_name:
                with st.spinner("PDF 문서 파싱 중..."):
                    raw_text = extract_text_from_pdf(uploaded_file)
                    
    else:
        url_input = st.text_input("웹사이트 URL 주소를 입력하세요:", placeholder="https://example.com/article")
        if url_input:
            source_name = url_input
            if "source_name" not in st.session_state or st.session_state.source_name != source_name:
                with st.spinner("웹페이지 텍스트 크롤링 중..."):
                    try:
                        raw_text = extract_text_from_url(url_input)
                    except Exception as e:
                        st.error(f"URL 로드 실패: {e}")

    # 데이터 저장
    if raw_text and source_name:
        st.session_state.pdf_text = raw_text
        st.session_state.pdf_chunks = split_into_chunks(raw_text)
        st.session_state.source_name = source_name
        st.session_state.chat_history = []
        st.success("🎉 자료 분석 완료! 하단 메뉴에서 학습을 진행해 주세요.")

    # 튜터 UI 실행
    if "pdf_chunks" in st.session_state:
        if not gemini_key:
            st.warning("⚠️ 왼쪽 사이드바에 Gemini API Key를 먼저 입력해주세요.")
        else:
            col1, col2 = st.columns([3, 2])

            with col1:
                st.markdown(f"#### 💬 1:1 대화형 질의응답 (`{st.session_state.source_name[:30]}...`)")
                chat_container = st.container()
                with chat_container:
                    for chat in st.session_state.chat_history:
                        if chat["role"] == "user":
                            st.markdown(f"**👤 나:** {chat['content']}")
                        else:
                            st.info(f"**🤖 AI 튜터:**\n{chat['content']}")

                user_question = st.text_input("내용에 대해 질문해 보세요:", key="tutor_question")
                if st.button("질문 전송", key="btn_send_tutor") and user_question:
                    relevant_context = find_relevant_chunks(user_question, st.session_state.pdf_chunks)
                    prompt = f"""
                    다음 제공된 [참고 자료]를 바탕으로 사용자의 [질문]에 대해 핵심만 요약하여 3문장 이내의 존댓말로 명확하게 답변해주세요.
                    [참고 자료]
                    {"\\n\\n".join(relevant_context)}
                    
                    [질문]
                    {user_question}
                    """
                    with st.spinner("생각 중..."):
                        try:
                            response = model.generate_content(prompt)
                            st.session_state.chat_history.append({"role": "user", "content": user_question})
                            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                            st.rerun()
                        except Exception as e:
                            st.error(f"오류: {e}")

            with col2:
                st.markdown("#### 📝 요약 및 퀴즈 출제")
                if st.button("본문 핵심 요약하기", key="btn_summary"):
                    sample_text = "\\n\\n".join(st.session_state.pdf_chunks[:6])
                    prompt = f"다음 글의 핵심 내용을 구조화된 리스트 형태로 한국어 요약해줘.\\n\\n[글]\\n{sample_text}"
                    with st.spinner("요약 작성 중..."):
                        try:
                            response = model.generate_content(prompt)
                            st.session_state.tutor_summary = response.text
                        except Exception as e:
                            st.error(f"요약 실패: {e}")

                if "tutor_summary" in st.session_state:
                    st.info(st.session_state.tutor_summary)

                if st.button("자가진단 퀴즈 3문항 생성", key="btn_quiz"):
                    sample_text = "\\n\\n".join(st.session_state.pdf_chunks[:6])
                    prompt = f"다음 글을 바탕으로 기말고사 대비 객관식 문제 3문항과 상세 해설을 한국어로 작성해줘.\\n\\n[글]\\n{sample_text}"
                    with st.spinner("퀴즈 생성 중..."):
                        try:
                            response = model.generate_content(prompt)
                            st.session_state.tutor_quiz = response.text
                        except Exception as e:
                            st.error(f"퀴즈 생성 실패: {e}")

                if "tutor_quiz" in st.session_state:
                    st.markdown(st.session_state.tutor_quiz)
    else:
        st.info("💡 위의 입력창을 사용해 PDF 파일을 첨부하거나 사이트 URL 주소를 입력하면 인공지능이 분석을 시작합니다.")

# ------------------------------------------------------------------
# 뉴스 감성 분석 유틸리티 함수 (성능 최적화 캐시 적용)
# ------------------------------------------------------------------
@st.cache_data(ttl=300) # 5분간 크롤링 데이터 캐싱
def fetch_google_news(keyword):
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            root = ET.fromstring(r.read())
            # 기사 개수를 7개로 줄여 속도 단축
            return [{"title": item.find('title').text, "link": item.find('link').text} for item in root.findall('.//item')[:7]]
    except Exception:
        return []

@st.cache_data(ttl=600) # 10분간 AI 분석 결과 캐싱 (중복 호출 및 대기 시간 단축)
def get_gemini_sentiment_analysis(titles_input, gemini_key):
    try:
        genai.configure(api_key=gemini_key)
        temp_model = genai.GenerativeModel('gemini-1.5-flash')
        # 불필요한 토큰 생성을 줄이기 위해 JSON 구조 간소화 및 reason 필드 삭제
        prompt = f"""
        뉴스 제목들을 분석하여 긍정, 부정, 중립 감성 분류를 처리하고, 지정된 JSON 형식으로 한국어 응답을 반환해 주세요.
        토큰 생성을 줄이고 연산 속도를 극대화하기 위해, summary는 20자 이내의 아주 짧은 1줄로 축약해 작성해야 합니다.
        
        [기사 목록]
        {titles_input}

        [JSON 응답 스키마]
        {{
          "summary": "시장 분위기 1줄 요약",
          "results": [
            {{"id": 0, "sentiment": "긍정" | "부정" | "중립"}}
          ]
        }}
        """
        res = temp_model.generate_content(prompt).text.strip()
        return res
    except Exception as e:
        return f"Error: {e}"

# ------------------------------------------------------------------
# 탭 2: 실시간 뉴스 감성 분석
# ------------------------------------------------------------------
with tab_sentiment:
    st.markdown("### 📈 실시간 뉴스 여론 트렌드 분석")
    search_keyword = st.text_input("검색할 주식 종목명, 기업명 또는 기술 트렌드를 입력하세요:", placeholder="예: 삼성전자, 엔비디아, LLM")
    
    if search_keyword:
        if not gemini_key:
            st.warning("⚠️ 왼쪽 사이드바에 Gemini API Key를 입력해 주세요.")
        else:
            with st.spinner("뉴스 피드 가져오는 중..."):
                news_list = fetch_google_news(search_keyword)

            if not news_list:
                st.info("최근 검색된 뉴스가 없습니다.")
            else:
                titles_input = "\\n".join([f"[{i}] {n['title']}" for i, n in enumerate(news_list)])

                with st.spinner("AI가 각 기사 여론의 긍정/부정 판단 중..."):
                    try:
                        res = get_gemini_sentiment_analysis(titles_input, gemini_key)
                        if res.startswith("Error:"):
                            raise ValueError(res)
                            
                        if "```
```text?code_stderr&code_event_index=2
Traceback (most recent call last):
  File "<xbox-string>", line 27
    font-size: 2.8rem;
                 ^
SyntaxError: invalid decimal literal

```json" in res:
                            res = res.split("```json")[1].split("```")[0]
                        elif "```" in res:
                            res = res.split("```")[1].split("```")[0]
                        
                        data = json.loads(res.strip())

                        p_cnt = sum(1 for r in data["results"] if r["sentiment"] == "긍정")
                        n_cnt = sum(1 for r in data["results"] if r["sentiment"] == "부정")
                        neu_cnt = sum(1 for r in data["results"] if r["sentiment"] == "중립")

                        st.markdown("---")
                        col_stat1, col_stat2, col_stat3 = st.columns(3)
                        col_stat1.metric("🟢 긍정 뉴스", f"{p_cnt}건")
                        col_stat2.metric("🔴 부정 뉴스", f"{n_cnt}건")
                        col_stat3.metric("⚪ 중립 뉴스", f"{neu_cnt}건")

                        col_l, col_r = st.columns([1, 1])
                        with col_l:
                            st.markdown("#### 📊 여론 감성 차트")
                            fig = go.Figure(data=[go.Pie(
                                labels=['긍정', '부정', '중립'], 
                                values=[p_cnt, n_cnt, neu_cnt], 
                                hole=.4,
                                marker=dict(colors=['#10B981', '#EF4444', '#9CA3AF'])
                            )])
                            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10), height=300)
                            st.plotly_chart(fig, use_container_width=True)

                        with col_r:
                            st.markdown("#### 📝 AI 종합 분석 리포트")
                            st.info(data["summary"])

                        st.markdown("#### 📰 뉴스 기사별 상세 감성 결과")
                        for idx, item in enumerate(data["results"]):
                            if idx < len(news_list):
                                sent = item["sentiment"]
                                badge = "sentiment-neutral"
                                if sent == "긍정": badge = "sentiment-positive"
                                elif sent == "부정": badge = "sentiment-negative"

                                st.markdown(f\"\"\"
                                <div style="padding: 12px; border: 1px solid #E2E8F0; border-radius: 6px; margin-bottom: 8px;">
                                    <span class="{badge}">{sent}</span>
                                    <a href="{news_list[idx]['link']}" target="_blank" style="font-weight: bold; text-decoration: none; color: #2563EB; margin-left: 8px;">
                                        {news_list[idx]['title']}
                                    </a>
                                </div>
                                \"\"\", unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"분석 중 에러가 발생했습니다: {e}")
"""

# Let's remove comments for the no-comment version.
# We need to be careful not to remove URL strings or string literals starting with #, or CSS color codes.
# A simple regex approach or line-by-line split.
lines = app_code.split('\n')
no_comment_lines = []
for line in lines:
    stripped = line.strip()
    # If the line itself is a comment line
    if stripped.startswith('#') and not stripped.startswith('#3B82F6') and not stripped.startswith('#D1FAE5') and not stripped.startswith('#065F46') and not stripped.startswith('#FEE2E2') and not stripped.startswith('#991B1B') and not stripped.startswith('#F3F4F6') and not stripped.startswith('#374151') and not stripped.startswith('#10B981') and not stripped.startswith('#EF4444') and not stripped.startswith('#9CA3AF') and not stripped.startswith('#E2E8F0') and not stripped.startswith('#2563EB'):
        # It's a full line comment
        continue
    # Inline comment removal? Be careful with strings. Let's just remove obvious standalone comments or lines.
    # To be perfectly safe, let's look for '  # ' or ' # ' but avoid string literals.
    # Given the clean code, removing lines starting with # handles most section headers.
    no_comment_lines.append(line)

no_comment_code = '\n'.join(no_comment_lines)

# Write files to check
with open('app_with_comments.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

# Clean up code lines that are purely comments
clean_no_comment_lines = []
for line in lines:
    if line.strip().startswith('#') and '-' not in line and '1.' not in line and '2.' not in line and '3.' not in line and '4.' not in line and '5.' not in line:
        continue
    if line.strip().startswith('#') and ('---' in line or '유틸리티' in line or '탭' in line or '페이지' in line or '스타일' in line or 'API' in line or '사이드바' in line or 'Gemini' in line):
        continue
    # handle basic trailing comments if any
    clean_no_comment_lines.append(line)

with open('app_no_comments.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(clean_no_comment_lines))

print("Files generated successfully.")