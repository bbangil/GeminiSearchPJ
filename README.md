# Gemini Developer Assistant (GeminiSearchPJ)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Vertex%20AI-orange?style=for-the-badge&logo=google&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-CLI%20UI-green?style=for-the-badge)

**Gemini Developer Assistant**는 구글의 최신 생성형 AI인 **Gemini 2.0 Flash** 모델을 활용하여 개발자의 생산성을 극대화하기 위해 설계된 **CLI(Command Line Interface) 기반의 AI 비서 도구**입니다.

터미널 환경에서 벗어나지 않고 즉각적으로 기술 질문을 해결하거나, 작성 중인 코드를 정밀하게 리뷰받아 리팩토링 제안을 받을 수 있습니다. 모든 상호작용은 자동으로 로깅되어 이력을 추적할 수 있으며, 코드 리뷰 결과는 별도의 마크다운 파일로 자동 저장되어 팀원들과 공유하거나 문서화하기 용이합니다.

---

## 🚀 Key Features

### 1. 💬 AI Chat Interface (General Query)
- **즉각적인 문제 해결:** 터미널에서 바로 Gemini에게 기술적인 질문을 던지고 답변을 받을 수 있습니다.
- **Rich Text Rendering:** `rich` 라이브러리를 사용하여 마크다운(Markdown) 형식의 답변을 터미널에서 가독성 높게 렌더링합니다.
- **스트리밍 응답:** 답변이 생성되는 즉시 스트리밍으로 출력되어, 긴 답변도 지루함 없이 확인할 수 있습니다.

### 2. 🧐 Automated Code Review
- **심층 코드 분석:** 특정 소스 파일을 지정하면, Gemini가 수석 아키텍트의 관점에서 코드를 라인별로 분석합니다.
- **자동 문서화:** 리뷰 결과는 `CodeReview/REVIEW_{파일명}.md` 형식으로 자동 저장됩니다.
- **개선 제안:** 성능 최적화, 보안 취약점 점검, 클린 코드 원칙에 입각한 구체적인 개선안을 제시합니다.

### 3. 📜 History Logging
- **이력 추적:** 수행된 모든 명령어와 질문 유형(일반 질문/코드 리뷰)은 `GeminiLog/history.log`에 타임스탬프와 함께 자동으로 기록됩니다.
- **학습 데이터 활용:** 과거의 질문과 해결 과정을 쉽게 찾아보고, 개인 지식 데이터베이스로 활용할 수 있습니다.

---

## 🛠 Tech Stack

- **Language:** Python 3.10+
- **AI Model:** Google Gemini 2.0 Flash (via Vertex AI)
- **Libraries:**
  - `google-genai`: Google GenAI SDK
  - `google-auth`: 인증 관리
  - `rich`: 터미널 UI 및 마크다운 렌더링
  - `argparse`: CLI 명령어 파싱

---

## ⚙️ Installation

1. **Repository Clone**
   ```bash
   git clone https://github.com/username/GeminiSearchPJ.git
   cd GeminiSearchPJ
   ```

2. **가상 환경 생성 및 활성화**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   # venv\Scripts\activate  # Windows
   ```

3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **Google Cloud 인증 설정**
   Google Cloud CLI(gcloud)가 설치되어 있어야 하며, Vertex AI API가 활성화된 프로젝트에 로그인되어 있어야 합니다.
   ```bash
   gcloud auth application-default login
   ```

---

## 📖 Usage

### 1. 일반 질문 (General Query)
간단한 기술 질문이나 개념 설명이 필요할 때 사용합니다.
```bash
python gemini_chat.py "Python 비동기 프로그래밍의 장점은?"
```

### 2. 코드 리뷰 (Code Review)
작성한 코드를 AI에게 리뷰받고 싶을 때 `-r` 옵션을 사용합니다.
```bash
python gemini_chat.py -r ./path/to/your/file.py
```
> **Output:** `CodeReview/REVIEW_file.py.md` 파일이 생성됩니다.

### 3. 히스토리 확인 (History)
과거의 명령어 사용 이력을 확인합니다.
```bash
python gemini_chat.py -l
```

---

## 📂 Project Structure

```
GeminiSearchPJ/
├── gemini_chat.py       # 메인 실행 파일 (CLI 진입점)
├── requirements.txt     # 프로젝트 의존성 목록
├── GeminiLog/           # [Auto-generated] 활동 로그 저장소
│   └── history.log      # 실행 이력 기록
└── CodeReview/          # [Auto-generated] 코드 리뷰 결과 저장소
    └── REVIEW_xxx.md    # 생성된 코드 리뷰 마크다운 파일
```

---

## 💡 Motivation & Architecture

이 프로젝트는 개발자가 IDE와 브라우저(ChatGPT 등)를 오가며 발생하는 **컨텍스트 스위칭(Context Switching) 비용을 최소화**하기 위해 시작되었습니다.

- **Architecture Pattern:** 단순함을 위해 절차적 프로그래밍과 함수형 스타일을 혼합하여 작성되었으며, `Client` 객체 생성과 비즈니스 로직(`handle_general_query`, `handle_code_review`)을 분리하여 유지보수성을 높였습니다.
- **Log Strategy:** 모든 활동을 파일 시스템에 로깅하여, 추후 데이터 분석이나 개인화된 AI 튜닝에 활용할 수 있는 기반을 마련했습니다.

---

## 📝 License

This project is licensed under the MIT License.
