# 🎓 깃허브(GitHub) 기말 프로젝트 업로드 최종 정리 가이드

이 문서는 본 프로젝트 폴더(`AI-Data-Analyzer`)의 모든 구성 요소를 본인의 깃허브 저장소에 성공적으로 업로드하고, 제출 조건에 맞추어 팀 협업 흔적을 남기는 방법을 최종 정리한 매뉴얼입니다.

---

## 📂 1. 업로드 대상 파일 구조 (Checklist)

깃허브 레포지토리에 올라가야 할 필수 파일들입니다.

*   `app.py`: 통합 웹 애플리케이션 핵심 소스코드.
*   `requirements.txt`: 제3자 실행용 패키지 의존성 목록.
*   `README.md`: 팀원 소개, 역할 분담, 실행 방법 및 데모 캡처 링크가 적힌 프로젝트 메인 대문.
*   `prompt_history.md`: 개발 과정에서 AI와 나눈 프롬프트 설계 역사 기록.
*   `.gitignore`: 로컬 키(`secrets.toml`) 및 시스템 캐시 파일이 업로드되지 않게 막는 예외 처리 파일.
*   `run.bat`: 제3자가 더블클릭 한 번으로 가상환경을 구축해 실행할 수 있게 돕는 자동화 스크립트.
*   `setup_github.bat`: 복잡한 Git 명령어 입력 없이 저장소를 바로 업로드해 주는 자동화 윈도우 스크립트.

---

## 🚀 2. 자동 업로드 방법 (윈도우용)

1.  본인의 깃허브(GitHub) 계정에 로그인하여 **새 Public(전체공개) 저장소**를 생성합니다.
2.  저장소의 주소를 복사합니다. (예: `https://github.com/내아이디/레포명.git`)
3.  본 폴더(`AI-Data-Analyzer`)에 있는 `setup_github.bat` 파일을 더블 클릭하여 실행합니다.
4.  안내창이 뜨면 복사한 **깃허브 저장소 주소를 입력하고 엔터**를 누릅니다.
5.  깃허브 로그인 창이 나타나면 로그인을 수행합니다. 
6.  업로드가 즉시 진행되며 완료 후 터미널 창이 꺼집니다. 깃허브 웹페이지를 새로고침하면 모든 소스코드가 들어가 있는 것을 볼 수 있습니다.

---

## 🛠️ 3. 수동 업로드 방법 (Git Bash 또는 터미널용)

자동화 스크립트가 실행되지 않거나 Mac/Linux 환경에서 수동으로 업로드할 때 사용하는 표준 Git 명령어입니다.

```bash
# 1. 저장소 초기화 및 원격 연결
git init
git remote add origin [내_깃허브_레포지토리_주소]

# 2. 업로드할 파일 추가 및 첫 커밋 생성
git add .
git commit -m "feat: 기말 프로젝트 통합 AI Assistant 배포 및 속도 최적화 적용"

# 3. 메인 브랜치 설정 및 최종 푸시
git branch -M main
git push -u origin main
```

---

## 👥 4. 제출 조건 만족을 위한 팀 협업 가이드 (Branch & PR)

과제 제출 시 **"팀원 간 브랜치를 파서 작업한 뒤 PR 승인을 거쳐 main에 머지"**하는 과정이 깃 로그에 반드시 보여야 합니다. 첫 코드가 올라간 후 아래 규칙을 지켜 작업하세요.

1.  **각 팀원의 개별 브랜치 생성**:
    *   예: 홍길동 팀원은 `feature/pdf-tutor`, 이순신 팀원은 `feature/news-sentiment` 브랜치를 생성해 작업합니다.
    ```bash
    git checkout -b feature/pdf-tutor
    ```
2.  **작업 후 개인 브랜치로 푸시**:
    ```bash
    git add .
    git commit -m "docs: README 팀원 기여도 및 설명 수정"
    git push origin feature/pdf-tutor
    ```
3.  **Pull Request (PR) 및 코드 리뷰**:
    *   GitHub 웹 저장소 페이지로 들어오면 **"Compare & pull request"** 버튼이 나타납니다.
    *   이를 클릭하여 작업 상세 내용을 적고 PR을 올린 뒤, 다른 팀원이 코드를 보고 승인(Approve) 리뷰를 남긴 후 **[Merge pull request]** 버튼을 눌러 main에 병합합니다.

이 가이드 파일(`github_upload_manual.md`)은 보관용으로 이 폴더에 두고 사용하셔도 되며, 깃에 커밋해서 함께 올리셔도 과제 가독성에 큰 도움이 됩니다!
