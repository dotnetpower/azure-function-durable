# Azure Functions - Durable Function

이 리포지토리는 Azure Durable Functions을 .NET(C#)과 Python으로 구현한 예제를 포함합니다.

## 📁 프로젝트 구조

```
.
├── dotnet/          # .NET(C#) 구현
│   ├── Orchestrations/
│   │   ├── Activities/
│   │   └── BlobJob/
│   └── Tirggers/
│
├── python/          # Python 구현
│   ├── Orchestrations/
│   │   ├── Activities/
│   │   └── BlobJob/
│   ├── Triggers/
│   └── examples/
│       ├── ai_agent_workflow.py  # AI Agent 워크플로 예제
│       └── README.md
│
└── README.md
```

---

## 🎯 Durable Functions란?

**Durable Functions**는 서버리스 환경에서 **상태 저장(stateful) 함수**를 작성할 수 있게 해주는 Azure Functions의 확장 기능입니다. 코드를 사용하여 서버리스 컴퓨팅 환경에서 상태 저장 워크플로를 정의할 수 있습니다.

### 주요 이점
- ✅ **상태 관리 자동화**: 함수 실행 중 상태를 자동으로 체크포인트하고 복원
- ✅ **긴 시간 실행**: 몇 분에서 몇 시간, 심지어 며칠까지 실행 가능
- ✅ **재시도 및 복구**: 자동 재시도 및 오류 처리
- ✅ **확장성**: Azure의 자동 확장 기능 활용

### 🤖 AI Agent Workflow Orchestration

Durable Functions는 **AI 에이전트의 복잡한 워크플로를 조정**하는 데 이상적입니다. 여러 AI 모델과 서비스를 조합하여 지능형 자동화를 구현할 수 있습니다.

**AI Agent 사용 사례:**

1. **Multi-Agent 협업 시스템**
   ```
   사용자 입력 → 의도 분석 Agent → 작업 분배 Orchestrator
                                          ├→ 검색 Agent (RAG)
                                          ├→ 코드 생성 Agent
                                          └→ 요약 Agent
                                          ↓
                                    결과 통합 및 응답
   ```

2. **장기 실행 AI 파이프라인**
   - 대용량 문서 분석 및 요약
   - 멀티모달 콘텐츠 생성 (텍스트 → 이미지 → 비디오)
   - 반복적인 모델 학습 및 평가

3. **Human-in-the-Loop AI 워크플로**
   ```
   AI 초안 생성 → 사람 검토 대기 → 피드백 반영 → 재생성
   ```

4. **분산 AI 추론**
   - 여러 LLM 모델에 동시 요청 (GPT, Claude, Gemini)
   - 결과 비교 및 앙상블
   - 최적의 응답 선택

**예시: AI 문서 처리 워크플로**
```python
# Orchestrator: 문서 처리 파이프라인
async def ai_document_processor(context):
    document = context.get_input()
    
    # 1. 문서 분류 (AI Agent)
    category = await context.call_activity('classify_document', document)
    
    # 2. 병렬 처리 (Fan-out)
    tasks = [
        context.call_activity('extract_entities', document),      # NER
        context.call_activity('summarize_content', document),     # 요약
        context.call_activity('analyze_sentiment', document),     # 감성 분석
        context.call_activity('generate_keywords', document)      # 키워드 추출
    ]
    results = await asyncio.gather(*tasks)
    
    # 3. 결과 통합 (Fan-in)
    final_result = await context.call_activity('merge_results', {
        'category': category,
        'entities': results[0],
        'summary': results[1],
        'sentiment': results[2],
        'keywords': results[3]
    })
    
    return final_result
```

**AI Agent에 Durable Functions를 사용하는 이유:**
- 🔄 **장시간 실행**: LLM 추론, 임베딩 생성 등 시간이 오래 걸리는 작업 처리
- 🔁 **재시도 로직**: API 레이트 리밋, 타임아웃 등 외부 AI 서비스 장애 대응
- 🎯 **조건부 실행**: AI 응답에 따라 다른 에이전트로 라우팅
- 💾 **상태 유지**: 대화 컨텍스트, 중간 결과 자동 저장
- 🔀 **병렬 처리**: 여러 AI 모델 동시 호출로 응답 속도 향상

---

## 📚 Durable Functions의 주요 패턴

Durable Functions는 다음과 같은 일반적인 애플리케이션 패턴을 지원합니다:

### 1️⃣ **Function Chaining (함수 체이닝)**
여러 함수를 특정 순서대로 실행하는 패턴입니다. 한 함수의 출력이 다음 함수의 입력이 됩니다.

![Function Chaining Pattern](https://learn.microsoft.com/ko-kr/azure/azure-functions/durable/media/durable-functions-concepts/function-chaining.png)

**사용 사례:**
- 순차적인 데이터 처리 파이프라인
- ETL(추출, 변환, 로드) 프로세스
- 다단계 승인 워크플로

**특징:**
- 각 단계의 결과를 다음 단계로 전달
- 중간 단계 실패 시 자동 재시도 가능
- 전체 체인의 상태를 추적 및 모니터링

### 2️⃣ **Fan-out/Fan-in (팬아웃/팬인)**
여러 함수를 병렬로 실행한 다음, 모든 함수가 완료될 때까지 기다리는 패턴입니다.

![Fan-out/Fan-in Pattern](https://learn.microsoft.com/ko-kr/azure/azure-functions/durable/media/durable-functions-concepts/fan-out-fan-in.png)

**사용 사례:**
- 대량의 데이터를 병렬로 처리
- 여러 외부 API를 동시에 호출하고 결과 집계
- 대규모 배치 작업

**특징:**
- 작업을 여러 인스턴스로 분산(Fan-out)
- 모든 병렬 작업이 완료될 때까지 대기
- 결과를 수집하고 집계(Fan-in)
- 처리량과 성능 향상

### 3️⃣ **Async HTTP APIs (비동기 HTTP API)**
장기 실행 작업의 상태를 폴링하는 패턴입니다. HTTP 웹훅을 통해 비동기 작업을 조정합니다.

![Async HTTP APIs Pattern](https://learn.microsoft.com/ko-kr/azure/azure-functions/durable/media/durable-functions-concepts/async-http-api.png)

**사용 사례:**
- 오래 걸리는 데이터 처리 작업
- 외부 시스템 통합
- 리포트 생성

**특징:**
- 즉시 202 Accepted 응답 반환
- 상태 확인 URL 제공
- 작업 완료 시 결과 반환
- 표준 HTTP 폴링 패턴 구현

### 4️⃣ **Monitor (모니터)**
워크플로에서 유연한 반복 프로세스를 구현하는 패턴입니다. 특정 조건이 충족될 때까지 주기적으로 확인합니다.

![Monitor Pattern](https://learn.microsoft.com/ko-kr/azure/azure-functions/durable/media/durable-functions-concepts/monitor.png)

**사용 사례:**
- 리소스 상태 모니터링
- 파일 도착 대기
- 외부 시스템의 작업 완료 대기
- 주기적인 헬스 체크

**특징:**
- 유연한 반복 간격 설정
- 만료 시간 설정 가능
- 조건 기반 종료
- 폴링 오버헤드 최소화

### 5️⃣ **Human Interaction (사람 개입)**
사람의 개입이 필요한 자동화 프로세스를 구현하는 패턴입니다. 승인 대기 등의 시나리오에 적합합니다.

![Human Interaction Pattern](https://learn.microsoft.com/ko-kr/azure/azure-functions/durable/media/durable-functions-concepts/approval.png)

**사용 사례:**
- 지출 승인 워크플로
- 문서 검토 및 승인
- 수동 검증이 필요한 프로세스

**특징:**
- 외부 이벤트 대기(승인/거부)
- 타임아웃 처리
- 에스컬레이션 로직
- 사람과 자동화의 결합

### 6️⃣ **Aggregator (Stateful Entities)**
여러 소스의 이벤트 데이터를 단일 엔터티로 집계하는 패턴입니다. Durable Entities를 사용합니다.

![Aggregator Pattern](https://learn.microsoft.com/ko-kr/azure/azure-functions/durable/media/durable-functions-concepts/aggregator.png)

**사용 사례:**
- IoT 디바이스 데이터 집계
- 게임 점수 집계
- 쇼핑 카트 관리
- 실시간 대시보드

**특징:**
- 작은 단위의 엔터티로 상태 관리
- 동시성 제어
- 직접 주소 지정 가능
- 이벤트 소싱 패턴 구현

---

## 🔧 Durable Functions의 구성 요소

### **Orchestrator 함수**
워크플로의 진행을 조정하고 제어하는 함수입니다.

**특징:**
- 결정론적(deterministic)이어야 함
- 다른 함수들을 호출하고 조정
- 상태를 자동으로 체크포인트
- 재실행 시 멱등성 보장

**제약사항:**
- 난수 생성, 현재 시간 등 비결정적 코드 사용 불가
- 네트워크/데이터베이스 직접 호출 불가 (Activity를 통해서만)
- 무한 루프 사용 불가

### **Activity 함수**
실제 작업을 수행하는 기본 작업 단위입니다.

**특징:**
- 실제 비즈니스 로직 수행
- 외부 시스템 호출 가능
- 입력과 출력 처리
- 재시도 정책 적용 가능

**사용 예:**
- 데이터베이스 쿼리
- 파일 처리
- 외부 API 호출
- 계산 작업

### **Client 함수**
Orchestrator를 시작하고 관리하는 함수입니다.

**기능:**
- Orchestrator 인스턴스 시작
- 인스턴스 상태 쿼리
- 이벤트 전송
- 인스턴스 종료

---

## 🚀 시작하기

### .NET (C#) 버전

#### 1. 의존성 복원
```bash
cd dotnet
dotnet restore
```

#### 2. local.settings.json 설정
`dotnet` 폴더에 `local.settings.json` 파일 생성:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true 또는 실제 Storage 연결 문자열",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet",
    "IoTHubConnectionString": "Built-in endpoints > Event Hub compatible endpoint",
    "SqlConnectionString": "SQL Server 연결 문자열",
    "AzureWebJobs.SQLTrigger.Disable": "true"
  }
}
```

#### 3. 실행
```bash
func start
```

### Python 버전

#### 1. uv 설치 (필요한 경우)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# 또는
pip install uv
```

#### 2. 프로젝트 설정 및 패키지 설치
```bash
cd python
uv sync
```

#### 3. 환경 변수 설정
`.env.example` 파일을 복사하여 `.env` 파일 생성 후 실제 값으로 수정:

```bash
cp .env.example .env
```

`.env` 파일 예시:
```env
AzureWebJobsStorage=UseDevelopmentStorage=true
FUNCTIONS_WORKER_RUNTIME=python
IoTHubConnectionString=Endpoint=sb://...
SqlConnectionString=Server=...
AzureWebJobs.SQLTrigger.Disable=true
```

**참고**: Azure Functions는 `local.settings.json`도 지원하지만, `.env` 파일을 사용하면 더 간편하게 환경 변수를 관리할 수 있습니다.

#### 4. 실행
```bash
uv run func start
```

---

## 🔄 동작 방식 (Function Chaining 예제)

이 프로젝트는 **Function Chaining** 패턴을 구현합니다:

```
IoT Hub → IoTHub_Trigger → BlobJobOrchestrator → BlobJobActivity1
(Client)                    (Orchestrator)        (Activity)
```

### 호출 흐름

1. **IoT Hub 이벤트 발생**: 디바이스에서 IoT Hub로 메시지 전송
2. **IoTHub_Trigger 실행**: 이벤트를 받아 Durable Client로 동작
3. **BlobJobOrchestrator 시작**: Orchestrator 인스턴스 생성 및 시작
4. **BlobJobActivity1 호출**: 실제 작업 수행 (Activity)
5. **결과 반환**: Activity 결과를 Orchestrator가 수집

### .NET (C#) 구현 세부사항

IoT Hub 에 D2C 이벤트가 발생하면 다음처럼 EventHubTriggerAttribute를 IoTHubTrigger로 재정의한 어트리뷰트에서 트리거링 시작:

```csharp
using IoTHubTrigger = Microsoft.Azure.WebJobs.EventHubTriggerAttribute;
```

`/Triggers/IoTHub_Trigger.cs`의 Run() 함수 시그니처:

```csharp
public async Task Run(
    [IoTHubTrigger("messages/events", Connection = "IoTHubConnectionString")]EventData message, 
    [DurableClient]IDurableClient orchestratorClient,
    ILogger log)
```

---

## 🗄️ SQL Trigger

SQL Database의 변경사항을 감지하여 Azure Function을 트리거할 수 있습니다.

### 사전 요구사항

SQL Server에서 변경 추적 활성화:

```sql
-- 데이터베이스 레벨에서 변경 추적 활성화
ALTER DATABASE [your_database_name]
SET CHANGE_TRACKING = ON
(CHANGE_RETENTION = 2 DAYS, AUTO_CLEANUP = ON);

-- 테이블 레벨에서 변경 추적 활성화
ALTER TABLE [dbo].[your_table_name]
ENABLE CHANGE_TRACKING;
```

### 활성화

`local.settings.json`에서 SQL Trigger 활성화:

```json
{
  "Values": {
    "AzureWebJobs.SQLTrigger.Disable": "false"
  }
}
```

---

## 📖 참고 자료

- [Durable Functions 개요 (한국어)](https://learn.microsoft.com/ko-kr/azure/azure-functions/durable/durable-functions-overview)
- [Durable Functions 패턴](https://learn.microsoft.com/ko-kr/azure/azure-functions/durable/durable-functions-overview?tabs=csharp#application-patterns)
- [SQL Trigger 바인딩](https://learn.microsoft.com/ko-kr/azure/azure-functions/functions-bindings-azure-sql-trigger)
- [Python Durable Functions](https://learn.microsoft.com/ko-kr/azure/azure-functions/durable/quickstart-python-vscode)

---

## 🐛 디버깅 팁

**로컬 스토리지 에뮬레이터 없이 디버깅하는 경우:**
- Azure Portal에서 배포된 Function App을 **중지**해야 합니다
- 그래야 VSCode에서 breakpoint가 정상적으로 attach됩니다
- 하나의 Storage Account를 여러 Function App 인스턴스가 공유할 수 없기 때문입니다

---

## 📄 라이선스

MIT License
