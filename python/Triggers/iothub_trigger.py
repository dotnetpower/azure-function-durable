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
    logging.info(f'Python IoT Hub trigger function processed a message: {message_body}')
    
    # Durable Orchestration Client 생성
    client = df.DurableOrchestrationClient(starter)
    
    # Orchestrator 시작
    instance_id = await client.start_new(
        orchestration_function_name='blob_job_orchestrator',
        client_input=message_body
    )
    
    logging.info(f"Started Orchestrator with ID = '{instance_id}'...")
