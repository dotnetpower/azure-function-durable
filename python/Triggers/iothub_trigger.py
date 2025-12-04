import logging
import json
import azure.functions as func
import azure.durable_functions as df


async def main(
    event: func.EventHubEvent,
    starter: str
) -> None:
    """
    IoTHub_Trigger - IoT Hub의 이벤트를 받아 Durable Function Orchestrator를 시작
    
    Args:
        event: IoT Hub에서 전달된 EventHub 이벤트
        starter: Durable Orchestration Client
    """
    # 메시지 파싱
    message_body = event.get_body().decode('utf-8')
    # 보안: 민감한 데이터가 포함될 수 있는 메시지 내용은 로그에 기록하지 않음
    logging.info(f'Python IoT Hub trigger function processed a message. Length: {len(message_body) if message_body else 0}')
    
    # Durable Orchestration Client 생성
    client = df.DurableOrchestrationClient(starter)
    
    # Orchestrator 시작
    instance_id = await client.start_new(
        orchestration_function_name='blob_job_orchestrator',
        client_input=message_body
    )
    
    # 보안: Instance ID만 로그에 기록
    logging.info(f"Started Orchestrator with ID = '{instance_id}'")
