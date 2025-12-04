import logging
import azure.functions as func
import azure.durable_functions as df


def blob_job_activity1(message: str) -> str:
    """
    BlobJobActivity1 - Durable Function의 Activity 함수
    
    Args:
        message: Orchestrator로부터 전달받은 메시지
    
    Returns:
        처리 결과 문자열
    """
    logging.info(f"BlobJobActivity1 processing message: {message}")
    
    result = f"BlobJobActivity1: {message}"
    
    return result


# Activity 함수 빌더
activity = df.Activity.create(blob_job_activity1)
