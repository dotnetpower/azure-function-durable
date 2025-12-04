import logging
import azure.functions as func
import azure.durable_functions as df
from typing import Dict, List


def classify_document(document: str) -> str:
    """
    문서 분류 Activity
    AI 모델을 사용하여 문서 카테고리 결정
    """
    logging.info(f"Classifying document...")
    # 여기서 Azure OpenAI, Custom Vision 등 AI 서비스 호출
    # 예시: category = openai_client.classify(document)
    return "technical_report"


def extract_entities(document: str) -> List[Dict]:
    """
    개체명 인식 (NER) Activity
    문서에서 사람, 장소, 조직 등을 추출
    """
    logging.info(f"Extracting entities...")
    # Azure AI Language Service 또는 OpenAI 사용
    return [
        {"type": "PERSON", "text": "홍길동", "confidence": 0.95},
        {"type": "ORGANIZATION", "text": "Microsoft", "confidence": 0.92}
    ]


def summarize_content(document: str) -> str:
    """
    문서 요약 Activity
    긴 문서를 간결하게 요약
    """
    logging.info(f"Summarizing content...")
    # Azure OpenAI GPT-4 사용
    return "이 문서는 Azure Functions의 활용 방안에 대해 설명합니다..."


def analyze_sentiment(document: str) -> Dict:
    """
    감성 분석 Activity
    문서의 전반적인 감정 분석
    """
    logging.info(f"Analyzing sentiment...")
    # Azure AI Language Service 사용
    return {
        "sentiment": "positive",
        "confidence": 0.87,
        "scores": {"positive": 0.87, "neutral": 0.10, "negative": 0.03}
    }


def generate_keywords(document: str) -> List[str]:
    """
    키워드 추출 Activity
    문서의 주요 키워드 추출
    """
    logging.info(f"Generating keywords...")
    # Azure AI Language Service 또는 OpenAI 사용
    return ["Azure Functions", "Durable Functions", "AI Agent", "Workflow"]


def merge_results(data: Dict) -> Dict:
    """
    결과 통합 Activity
    모든 AI 분석 결과를 하나로 통합
    """
    logging.info(f"Merging all AI analysis results...")
    return {
        "document_category": data["category"],
        "entities": data["entities"],
        "summary": data["summary"],
        "sentiment": data["sentiment"],
        "keywords": data["keywords"],
        "processed_at": "2025-12-04T10:00:00Z"
    }


def ai_document_processor_orchestrator(context: df.DurableOrchestrationContext):
    """
    AI 문서 처리 Orchestrator
    여러 AI Agent를 조정하여 문서를 분석하는 복잡한 워크플로
    """
    document = context.get_input()
    logging.info(f"Starting AI document processing orchestration for document: {document[:50]}...")
    
    # 1. 문서 분류 (순차 실행)
    category = yield context.call_activity('classify_document_activity', document)
    logging.info(f"Document classified as: {category}")
    
    # 2. 병렬 AI 분석 (Fan-out/Fan-in 패턴)
    parallel_tasks = [
        context.call_activity('extract_entities_activity', document),
        context.call_activity('summarize_content_activity', document),
        context.call_activity('analyze_sentiment_activity', document),
        context.call_activity('generate_keywords_activity', document)
    ]
    
    # 모든 병렬 작업 완료 대기
    results = yield context.task_all(parallel_tasks)
    
    # 3. 결과 통합
    final_result = yield context.call_activity('merge_results_activity', {
        'category': category,
        'entities': results[0],
        'summary': results[1],
        'sentiment': results[2],
        'keywords': results[3]
    })
    
    logging.info(f"AI document processing completed. Instance ID: {context.instance_id}")
    return final_result


# Activity 함수 등록
classify_document_activity = df.Activity.create(classify_document)
extract_entities_activity = df.Activity.create(extract_entities)
summarize_content_activity = df.Activity.create(summarize_content)
analyze_sentiment_activity = df.Activity.create(analyze_sentiment)
generate_keywords_activity = df.Activity.create(generate_keywords)
merge_results_activity = df.Activity.create(merge_results)

# Orchestrator 함수 등록
ai_document_orchestrator = df.Orchestrator.create(ai_document_processor_orchestrator)
