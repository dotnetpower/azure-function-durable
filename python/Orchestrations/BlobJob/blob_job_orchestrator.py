import logging
import azure.functions as func
import azure.durable_functions as df


def blob_job_orchestrator(context: df.DurableOrchestrationContext):
    """
    BlobJobOrchestrator - Durable Function의 Orchestrator 함수
    IoTHub_Trigger에 의해 호출됨
    
    Args:
        context: Durable Orchestration Context
    
    Returns:
        Orchestration 결과
    """
    message = context.get_input()
    logging.info(f"BlobJobOrchestrator processed a message: {message}")
    
    # Activity 함수 호출
    result = yield context.call_activity('blob_job_activity1', message)
    
    # Orchestrator 인스턴스 ID 로깅
    logging.info(f"activity result: '{result}'")
    logging.info(f"Orchestration instance ID: {context.instance_id}")
    
    return result


# Orchestrator 함수 빌더
orchestrator = df.Orchestrator.create(blob_job_orchestrator)
