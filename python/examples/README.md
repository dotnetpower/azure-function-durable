# AI Agent Workflow 예제

이 예제는 Durable Functions를 사용하여 AI Agent의 복잡한 문서 처리 워크플로를 구현하는 방법을 보여줍니다.

## 워크플로 구조

```
문서 입력
    ↓
문서 분류 (AI Agent)
    ↓
병렬 AI 분석 (Fan-out/Fan-in)
    ├→ 개체명 인식 (NER)
    ├→ 문서 요약
    ├→ 감성 분석
    └→ 키워드 추출
    ↓
결과 통합
    ↓
최종 분석 결과
```

## 주요 구성 요소

### Orchestrator
- `ai_document_processor_orchestrator`: 전체 워크플로를 조정

### Activity Functions
1. `classify_document`: 문서 카테고리 분류
2. `extract_entities`: 개체명 인식 (NER)
3. `summarize_content`: 문서 요약
4. `analyze_sentiment`: 감성 분석
5. `generate_keywords`: 키워드 추출
6. `merge_results`: 모든 결과 통합

## 사용 방법

이 예제를 `function_app.py`에 통합하여 사용할 수 있습니다.

```python
from examples.ai_agent_workflow import (
    classify_document_activity,
    extract_entities_activity,
    summarize_content_activity,
    analyze_sentiment_activity,
    generate_keywords_activity,
    merge_results_activity,
    ai_document_orchestrator
)

# 각 Activity와 Orchestrator를 Function App에 등록
```

## AI 서비스 통합

실제 구현 시 다음 Azure AI 서비스와 통합할 수 있습니다:

- **Azure OpenAI Service**: GPT-4를 사용한 요약, 분류
- **Azure AI Language**: 개체명 인식, 감성 분석, 키워드 추출
- **Azure AI Document Intelligence**: 문서 구조 분석
- **Azure Cognitive Search**: RAG(검색 증강 생성)

## 실행 예시

HTTP 요청으로 Orchestrator 시작:

```bash
curl -X POST http://localhost:7071/api/orchestrators/ai_document_orchestrator \
  -H "Content-Type: application/json" \
  -d '{"document": "분석할 문서 내용..."}'
```

## 장점

1. **병렬 처리**: 여러 AI 분석을 동시에 실행하여 처리 시간 단축
2. **자동 재시도**: AI API 호출 실패 시 자동으로 재시도
3. **상태 관리**: 긴 문서 처리 중에도 상태가 자동으로 저장됨
4. **확장성**: 문서 수가 많아져도 자동으로 확장
