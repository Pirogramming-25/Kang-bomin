# Django GPT

Hugging Face `pipeline()` 모델을 Django 웹 서비스 기능으로 구성한 프로젝트입니다.
감정 분석, 문서 요약, 유해 표현 분석 기능을 각각 별도 URL로 제공하며, 세 모델을 순차적으로 연결하는 복합 분석 기능을 포함합니다.

## 기능 및 URL

| 탭 | URL | 접근 권한 |
| --- | --- | --- |
| 감정 분석 | `/sentiment/` | 비로그인 허용 |
| 문서 요약 | `/summarize/` | 로그인 필요 |
| 유해 표현 분석 | `/moderate/` | 로그인 필요 |
| 복합 분석 | `/combo/` | 로그인 필요 |

로그인/로그아웃은 Django 기본 인증 URL(`/accounts/login/`, `/accounts/logout/`)을 사용합니다.

## 실행 방법

### 1. 저장소 클론 및 가상환경 설정

```bash
git clone <repository-url>
cd Django_GPT
python -m venv venv
source venv\Scripts\activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

`.env.example`을 복사해 `.env` 파일을 만들고 값을 채워주세요.

```bash
cp .env.example .env
```

| 변수 | 설명 | 기본값 |
| --- | --- | --- |
| `HF_TOKEN` | Hugging Face API 토큰 (모델이 모두 공개 모델이라 비워둬도 동작하지만, Rate Limit 회피를 위해 설정 권장) | 없음 |
| `DEBUG` | Django 디버그 모드 여부 (`True`/`False`) | `True` |


### 4. 데이터베이스 마이그레이션 및 관리자 계정 생성

```bash
python manage.py migrate
python manage.py createsuperuser
```

`/summarize/`, `/moderate/`, `/combo/`는 로그인이 필요하므로, 위에서 만든 계정(또는 Django Admin에서 생성한 계정)으로 로그인해야 합니다.

### 5. 서버 실행

```bash
python manage.py runserver
```

`http://127.0.0.1:8000/` 접속 시 `/sentiment/`로 리다이렉트됩니다.

> 모델은 서버 시작 시 로드되지 않고, 각 기능을 처음 실행할 때 Lazy Loading되어 이후 요청부터는 캐시된 파이프라인을 재사용합니다. 따라서 각 탭을 처음 실행할 때는 모델 다운로드 및 로딩으로 시간이 걸릴 수 있습니다.

## 사용 모델

### 1. 감정 분석 (Sentiment Analysis)

- **Model ID:** [`cardiffnlp/twitter-roberta-base-sentiment-latest`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
- **License:** CC-BY-4.0
- **Task:** `text-classification`
- **입력 언어:** 영어
- **출력 레이블:** `negative`, `neutral`, `positive` (레이블 + 신뢰도 점수)
- **Service:** `my_gpt/services/sentiment.py`

### 2. 문서 요약 (Summarization)

- **Model ID:** [`sshleifer/distilbart-cnn-6-6`](https://huggingface.co/sshleifer/distilbart-cnn-6-6)
- **License:** Apache-2.0
- **Task:** `summarization`
- **입력 언어:** 영어
- **출력:** 요약문, 원문 길이, 요약문 길이, 요약 비율(%)
- **Service:** `my_gpt/services/summarizer.py`

### 3. 유해 표현 분석 (Toxicity Detection)

- **Model ID:** [`unitary/toxic-bert`](https://huggingface.co/unitary/toxic-bert)
- **License:** Apache-2.0
- **Task:** `text-classification` (Multi-label, `top_k=None`)
- **입력 언어:** 영어
- **출력 레이블:** `toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate` (전체 레이블 점수 내림차순 정렬)
- **Service:** `my_gpt/services/moderator.py`

## 복합 분석 (챌린지: 고객 피드백 분석 리포트)

`/combo/`는 위 세 모델을 아래 순서로 연결(Pipeline Chaining)합니다.

```
사용자 입력(영어 고객 리뷰/피드백)
  → ① 문서 요약 모델 실행 → 요약문 생성
  → ② 요약문을 감정 분석 모델에 입력 → Positive/Neutral/Negative
  → ③ 요약문을 유해 표현 분석 모델에 입력 → Toxicity Label
  → 결과 결합 및 조건문 기반 종합 판정 생성
```

감정 분석과 유해 표현 분석은 원문이 아닌 **1단계 요약 모델의 출력(요약문)**을 입력으로 사용합니다. (`my_gpt/services/combo.py`)

- **입력 조건:** 영어 고객 리뷰/피드백, 200~5,000자
- **재생성 기능:** "재생성" 버튼을 누르면 기존 원문을 그대로 사용해 요약 모델을 `do_sample=True, top_p=0.9, temperature=0.8` 옵션으로 다시 추론하고, 감정/유해 표현 분석도 새 요약문 기준으로 다시 실행합니다. (캐시된 결과를 재출력하지 않음)
- **종합 판정:** 별도 LLM 호출 없이 감정 레이블/유해 점수 조건문으로 생성합니다.

## 입력값 검증 기준

| 기능 | 최소 길이 | 최대 길이 |
| --- | --- | --- |
| 감정 분석 | 1자 | 1,000자 |
| 문서 요약 | 100자 | 5,000자 |
| 유해 표현 분석 | 1자 | 1,000자 |
| 복합 분석 | 200자 | 5,000자 |

모든 검증(빈 문자열/공백/길이/타입)은 Django View(`my_gpt/views.py`)에서 서버 측으로 수행하며, HTML `maxlength` 속성만으로는 검사하지 않습니다.

## 실행 기록

- 로그인 사용자가 모델을 실행하면 `InferenceHistory` 모델(`my_gpt/models.py`)에 입력값, 출력값, 구조화된 결과(`result_data`)가 저장됩니다.
- 각 탭은 `request.user`로 필터링된 본인의 최근 기록만 5개까지 최신순으로 표시합니다. 다른 사용자의 기록은 조회할 수 없습니다.
- 비로그인 사용자의 감정 분석 실행 기록은 DB에 저장하지 않고, 브라우저 메모리(JS 배열)에서만 최근 5개를 유지하며 새로고침 시 초기화됩니다.

## 아키텍처

- **Service 계층 분리:** 모델 실행 코드는 `my_gpt/views.py`에 직접 작성하지 않고 `my_gpt/services/{sentiment,summarizer,moderator,combo}.py`에서 처리합니다.
- **Lazy Loading & 캐시:** 각 파이프라인은 `functools.lru_cache(maxsize=1)`로 감싸져 있어 서버 시작 시가 아닌 최초 요청 시 로드되고, 이후 요청은 캐시된 객체를 재사용합니다.
- **공통 Device 설정:** `my_gpt/services/common.py`의 `get_pipeline_device()`가 CUDA → MPS → CPU 순으로 사용 가능한 디바이스를 자동 선택합니다.

## 보안

- `@csrf_exempt`를 사용하지 않으며, `fetch()` 요청에는 `X-CSRFToken` 헤더를 포함합니다.
- 로그인 필요 페이지는 커스텀 데코레이터(`my_gpt/decorators.py`)로 서버 측에서 접근을 제한하며, 브라우저 주소창으로 직접 접근해도 `/accounts/login/?next=<원래경로>&required=1`로 리다이렉트되고 로그인 후 원래 페이지로 복귀합니다.
- 모델 추론 실패 시 Python Traceback이나 Django Debug 페이지를 노출하지 않고, 서버 로그(`logger.exception`)만 남긴 뒤 사용자에게는 일반화된 오류 메시지를 반환합니다.
- Hugging Face 토큰은 코드에 하드코딩하지 않고 `.env`의 `HF_TOKEN` 환경변수로만 관리합니다.

## 기술 스택

```
Django 5.x
Django Template / JavaScript Fetch
Django ORM
Django Authentication / Session
CSRF Protection
Hugging Face Transformers (pipeline)
python-dotenv
HTML / CSS / JavaScript
```
