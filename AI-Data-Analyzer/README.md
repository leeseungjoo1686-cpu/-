# 🎓 Universal AI Assistant (PDF/URL Tutor & News Sentiment Dashboard)

본 프로젝트는 파이썬(Python)과 Streamlit 웹 프레임워크, 그리고 Google Gemini 1.5 API를 결합한 **RAG 기반 학습 보조 및 뉴스 여론 분석 웹 애플리케이션**입니다. 

팀 단위 프로젝트 제출 및 제3자가 프로젝트를 쉽게 복제하여 실행할 수 있도록 설계되었습니다.

---

## 👥 팀원 및 역할 (기여도)
> [!NOTE]
> 제출 전 팀원들의 이름과 학번, 역할 분담 및 실제 기여도(%)를 수정해 주세요.

| 이름 | 학번 | 역할 (Role) | 기여도 (Contribution) |
| :--- | :---: | :--- | :---: |
| **홍길동 (팀장)** | 20260001 | 프로젝트 총괄 기획, 1번 PDF/URL RAG 학습 보조 모델 구축 | **35%** |
| **이순신** | 20260002 | 2번 구글 뉴스 RSS 수집 연동 및 Gemini API 기반 감성 분석 구현 | **35%** |
| **임꺽정** | 20260003 | 웹 프론트엔드 CSS UI 커스텀 스타일링, 예외 처리, README 및 발표자료 작성 | **30%** |

---

## 📸 동작 화면 (Demo Screenshot / GIF)
> [!IMPORTANT]
> 실제로 돌아가는 모습을 캡처하여 `images` 폴더 등에 업로드한 후 아래 경로를 알맞게 변경해 주세요.

| 1. 문서 & 링크 튜터 (RAG) | 2. 실시간 뉴스 감성 분석 |
| :---: | :---: |
| ![Tutor Demo](https://raw.githubusercontent.com/username/repo/main/images/demo_tutor.png) | ![Sentiment Demo](https://raw.githubusercontent.com/username/repo/main/images/demo_sentiment.png) |

---

## 🚀 시작 가이드 (설치 및 실행 방법)
제3자가 깃허브 레포지토리를 복제(Clone)하여 실행하는 방법입니다.

### 방법 A: Windows 사용자 (원클릭 자동 실행)
레포지토리 최상위 경로에 있는 `run.bat` 파일을 더블 클릭하면 자동으로 파이썬 가상환경(`venv`) 생성, 필수 라이브러리 설치, 웹 서버 구동까지 자동으로 진행됩니다.
1. `run.bat` 실행
2. 브라우저에서 자동으로 열리는 웹사이트 확인

### 방법 B: 수동 실행 (터미널 명령어)
파이썬 3.9 이상이 설치된 환경에서 아래 명령어를 순서대로 실행합니다.

```bash
# 1. 레포지토리 복제 및 이동
git clone [우리_팀_레포지토리_주소.git]
cd AI-Data-Analyzer

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Mac/Linux
# Windows의 경우: venv\Scripts\activate

# 3. 필수 의존성 패키지 설치
pip install -r requirements.txt

# 4. Streamlit 서버 구동
streamlit run app.py
```

---

## 🛠️ 주요 사용 기술 및 아키텍처
*   **Python 3.9+**
*   **Frontend**: Streamlit (반응형 웹 UI 제공)
*   **AI Engine**: Google Gemini API (`gemini-1.5-flash`)
*   **Data Scraper**: PyPDF (로컬 PDF 파싱) & BeautifulSoup4 (웹사이트 본문 정제) & xml.etree.ElementTree (구글 뉴스 RSS 파서)
*   **Visualization**: Plotly (인터랙티브 도넛 차트 구현)

---

## 🔒 API 보안 수칙
*   개인의 API 키는 코드에 직접 하드코딩하지 않습니다.
*   웹 화면 좌측 사이드바의 입력 필드를 사용하여 안전하게 세션 내에 입력하여 구동되도록 설계되었습니다.
*   설정 파일(`.json` 등) 및 가상환경(`venv`)은 깃에 올라가지 않도록 `.gitignore` 설정이 되어 있습니다.
