@echo off
echo ===================================================
echo  AI Data Analyzer 실행 자동화 스크립트 (Windows용)
echo ===================================================
echo.
echo [1/3] 파이썬 가상환경(venv)을 확인하고 생성합니다...
if not exist venv (
    echo.
    echo 가상환경 venv가 존재하지 않아 새로 생성 중입니다...
    python -m venv venv
)
echo.
echo [2/3] 가상환경 활성화 및 필요 패키지 설치 진행 중...
call venv\Scripts\activate
pip install -r requirements.txt
echo.
echo [3/3] Streamlit 웹 애플리케이션 가동 중...
echo.
streamlit run app.py
pause
