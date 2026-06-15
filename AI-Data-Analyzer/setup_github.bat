@echo off
chcp 65001 > nul
echo ===================================================
echo  깃허브(GitHub) 자동 업로드 스크립트 (Windows용)
echo ===================================================
echo.
echo 이 스크립트는 현재 폴더의 모든 프로젝트 파일들을
echo 본인의 깃허브 저장소(Public)에 자동으로 업로드해 줍니다.
echo.
echo * 준비 사항: 깃허브 웹사이트에서 레포지토리를 미리 생성해 두세요.
echo.
set /p repo_url="1. 본인의 깃허브 저장소 주소(URL)를 입력하세요: "

if "%repo_url%"=="" (
    echo.
    echo [오류] 주소가 입력되지 않았습니다. 프로그램을 종료합니다.
    pause
    exit
)

echo.
echo [1/4] 로컬 Git 저장소 초기화 중...
git init

echo.
echo [2/4] 업로드할 파일 추가 및 첫 커밋 생성 중...
git add .
git commit -m "feat: 기말 프로젝트 통합 AI Assistant 초기 배포"

echo.
echo [3/4] 기본 브랜치를 main으로 설정하고 원격 저장소 연결 중...
git branch -M main
git remote remove origin >nul 2>&1
git remote add origin %repo_url%

echo.
echo [4/4] 깃허브 서버로 코드 업로드(Push) 진행 중...
echo (이 과정에서 깃허브 로그인 창이 뜰 수 있습니다. 로그인을 완료해 주세요.)
echo.
git push -u origin main

echo.
echo ===================================================
echo  업로드가 성공적으로 완료되었습니다! 
echo  웹 브라우저에서 깃허브 주소를 열어 파일이 들어갔는지 확인하세요.
echo ===================================================
pause
