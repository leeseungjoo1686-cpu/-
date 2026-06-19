import subprocess
import sys
import os
from pathlib import Path
import webbrowser

# ==========================================
# [원클릭 자동 실행] 실행 즉시 배포 사이트 오픈
# ==========================================
# 사용자가 이 파일을 더블 클릭하거나 실행하면 1초 만에 브라우저를 켭니다.
DEPLOYED_URL = "https://hb5gbjgc6vkkud5fub5mgb.streamlit.app/"

# Streamlit 환경이 아닌 로컬(cmd 등)에서 최초 실행될 때만 브라우저를 열도록 방어코드 삽입
if "STREAMLIT_SERVER_DIR" not in os.environ:
    webbrowser.open(DEPLOYED_URL)
    print(f"🚀 {DEPLOYED_URL} 주소로 브라우저를 자동 연결합니다.")

# ==========================================
# [기능 통합] 필수 라이브러리 자동 설치 엔진
# ==========================================
def install_missing_libraries():
    required_libraries = {
        "streamlit": "streamlit",
        "google.generativeai": "google-generativeai",
        "pandas": "pandas",
        "openpyxl": "openpyxl",
        "PIL": "pillow"
    }
    for module_name, pip_name in required_libraries.items():
        try:
            __import__(module_name)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])

install_missing_libraries()

import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image

# ==========================================
# 1. 디자인 및 테마 설정
# ==========================================
st.set_page_config(page_title="AI FILE ANALYZER", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600&family=IBM+Plex+Mono&display=swap');
    @import url('https://fonts.cdnfonts.com/css/cabinet-grotesk');
    * { font-family: 'IBM Plex Sans', sans-serif; }
    h1, h2, h3 { font-family: 'Cabinet Grotesk', sans-serif !important; font-weight: 900 !important; letter-spacing: -0.05em !important; color: #0A0A0A !important; }
    .stTextArea textarea { font-family: 'IBM Plex Mono', monospace !important; border-radius: 0px !important; border: 1px solid #E5E7EB !important; }
    .stButton>button { background-color: #0A0A0A !important; color: #FFFFFF !important; border-radius: 0px !important; border: none !important; padding: 0.75rem 2rem !important; font-weight: 600 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }
    .stButton>button:hover { background-color: #27272A !important; color: #FFFFFF !important; }
    .upload-label { font-size: 0.75rem !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.2em !important; color: #4B5563; margin-bottom: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. API 키 이중 방어 시스템 (기본키 내장 + 예외시 입력창)
# ==========================================
EMERGENT_BACKEND_LICENSE = "sk-emergent-eE5BbB3916024409d7"

st.title("AI FILE ANALYZER")

with st.expander("🔑 만약 'API Key Invalid' 에러가 발생한다면 여기를 클릭하세요"):
    custom_key = st.text_input("Google AI Studio에서 발급받은 무료 API Key를 입력하세요:", type="password")
    if custom_key:
        final_api_key = custom_key
    else:
        final_api_key = EMERGENT_BACKEND_LICENSE

def process_data_analysis(file_name, file_type, content_summary, custom_prompt=""):
    try:
        genai.configure(api_key=final_api_key)
        ai_engine = genai.GenerativeModel("gemini-2.5-flash")
        
        base_prompt = f"""
        당신은 수석 데이터 전문 분석가입니다. 
        제출된 파일 [{file_name}] ({file_type})의 통계 요약본을 보고 인사이트를 한국어로 요약하세요.
        
        [데이터 요약]
        {content_summary}
        
        [요청 사항]
        {custom_prompt if custom_prompt else "이 데이터의 유의미한 패턴을 분석해줘."}
        """
        response = ai_engine.generate_content(base_prompt)
        return response.text
    except Exception as e:
        if "API key not valid" in str(e):
            return "❌ **내장된 기본 API 키가 만료되었습니다.**\n\n상단의 **[🔑 만약 'API Key Invalid' 에러가 발생한다면...]** 열기를 눌러 본인의 무료 Gemini API 키를 넣어주시면 즉시 정상 작동합니다!"
        return f"데이터 스캔 중 오류가 발생했습니다: {str(e)}"

# ==========================================
# 3. UI 레이아웃
# ==========================================
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="upload-label">DATA SOURCE UPLOAD</div>', unsafe_allow_html=True)
    uploaded_raw_file = st.file_uploader("TXT, CSV, XLSX, PNG, JPG, PDF 지원", type=["txt", "csv", "xlsx", "png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
    
    st.markdown('<div class="upload-label" style="margin-top:2rem;">CUSTOM ANALYSIS FOCUS (OPTIONAL)</div>', unsafe_allow_html=True)
    user_focus_query = st.text_area("중점적으로 분석하고 싶은 질문을 적어주세요.", placeholder="예시: 이 데이터의 가장 큰 문제점 3가지만 뽑아줘", height=100)

with col2:
    st.markdown('<div class="upload-label">ANALYSIS REALTIME REPORT</div>', unsafe_allow_html=True)
    
    if uploaded_raw_file is not None:
        file_extension = Path(uploaded_raw_file.name).suffix.lower()
        extracted_data_body = ""
        
        try:
            if file_extension == ".csv":
                dataframe = pd.read_csv(uploaded_raw_file)
                st.dataframe(dataframe.head(5), use_container_width=True)
                extracted_data_body = f"구조: {dataframe.shape}\n요약:\n{dataframe.describe().to_string()}"
            elif file_extension == ".xlsx":
                dataframe = pd.read_excel(uploaded_raw_file)
                st.dataframe(dataframe.head(5), use_container_width=True)
                extracted_data_body = f"구조: {dataframe.shape}\n요약:\n{dataframe.describe().to_string()}"
            elif file_extension in [".png", ".jpg", ".jpeg"]:
                opened_image = Image.open(uploaded_raw_file)
                st.image(opened_image, width=350)
                extracted_data_body = f"이미지 해상도: {opened_image.size}"
            else:
                decoded_text = uploaded_raw_file.read().decode("utf-8", errors="ignore")
                st.text_area("문서 미리보기", decoded_text[:300] + "\n...", height=150, disabled=True)
                extracted_data_body = decoded_text

            if st.button("RUN ENGINE ANALYSIS"):
                with st.spinner("⚡ 연산 엔진 구동 중..."):
                    final_report = process_data_analysis(uploaded_raw_file.name, file_extension, extracted_data_body, user_focus_query)
                    st.markdown("---")
                    st.markdown(final_report)
                    
        except Exception as file_error:
            st.error(f"파일 분기 에러: {str(file_error)}")
    else:
        st.markdown("<div style='border: 1px dashed #E5E7EB; padding: 5rem; text-align: center; color: #9CA3AF; font-size: 0.875rem; font-family:\"IBM Plex Mono\";'>AWAITING DATA INGESTION...</div>", unsafe_allow_html=True)