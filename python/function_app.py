import logging
import azure.functions as func
import azure.durable_functions as df

# Import orchestrator and activity functions
from Orchestrations.Activities.blob_job_activity1 import blob_job_activity1
from Orchestrations.BlobJob.blob_job_orchestrator import blob_job_orchestrator

# Function App 생성 - 보안: FUNCTION 레벨 인증 사용
app = df.DFApp(http_auth_level=func.AuthLevel.FUNCTION)

# Activity 함수 등록
@app.activity_trigger(input_name="message")
def blob_job_activity1_func(message: str) -> str:
    return blob_job_activity1(message)

# Orchestrator 함수 등록
@app.orchestration_trigger(context_name="context")
def blob_job_orchestrator_func(context: df.DurableOrchestrationContext):
    return blob_job_orchestrator(context)

# IoT Hub Trigger 함수 등록
@app.event_hub_message_trigger(
    arg_name="event",
    event_hub_name="messages/events",
    connection="IoTHubConnectionString"
)
@app.durable_client_input(client_name="client")
async def iothub_trigger(event: func.EventHubEvent, client):
    """IoT Hub에서 이벤트를 받아 Durable Function Orchestrator를 시작"""
    message_body = event.get_body().decode('utf-8')
    # 보안: 민감한 데이터가 포함될 수 있는 메시지 내용은 로그에 기록하지 않음
    logging.info(f'Python IoT Hub trigger function processed a message. Length: {len(message_body) if message_body else 0}')
    
    # Orchestrator 시작
    instance_id = await client.start_new(
        orchestration_function_name='blob_job_orchestrator_func',
        client_input=message_body
    )
    
    # 보안: Instance ID만 로그에 기록
    logging.info(f"Started Orchestrator with ID = '{instance_id}'")

# HTTP Starter (테스트용) - 보안: FUNCTION 레벨 인증 적용
@app.route(route="orchestrators/{functionName}", auth_level=func.AuthLevel.FUNCTION)
@app.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    """HTTP 요청으로 Orchestrator를 시작하는 헬퍼 함수"""
    function_name = req.route_params.get('functionName')
    
    # 보안: function_name 입력 검증
    allowed_functions = ['blob_job_orchestrator_func']
    if function_name not in allowed_functions:
        return func.HttpResponse(
            "Invalid function name",
            status_code=400
        )
    
    instance_id = await client.start_new(function_name)
    
    response = client.create_check_status_response(req, instance_id)
    return response
