# azure-function-durable

로컬에서 실행 하려면 local.settings.json 파일을 다음과 같은 구조로 생성 필요. 
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "AzureWebJobsStorage connection string",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet",
    "IoTHubConnectionString": "Built-in endpoints > Event Hub compatible endpoint for service role"
  }
}
```
로컬 스토리지에뮬레이터 없이 로컬 디버깅을 하기위해서 서버에 배포된 Function App 을 중지 해야 VSCode 에서 breakpoint 가 attach 됨.

# 동작 방식(Durable Function)

- IoT Hub 에 D2C 이벤트가 발생하면 다음처럼 EventHubTriggerAttribute를 IoTHubTrigger로 재정의한 어트리뷰트에서 트리거링 시작
```C#
using IoTHubTrigger = Microsoft.Azure.WebJobs.EventHubTriggerAttribute
```
- /Triggers/IoTHub_Trigger.cs 의 Run() 함수의 기본 시그니처를 다음처럼 `[DurableClient]IDurableClient orchestratorClient` 가 추가되어야 함
 ```C#
 public async Task Run(
            [IoTHubTrigger("messages/events", Connection = "IoTHubConnectionString")]EventData message, 
            [DurableClient]IDurableClient orchestratorClient,
            ILogger log)
 ```
 
 ## 호출 순서(namespace 생략)
 IoTHub_Trigger -> BlobJobOrchestrator -> BlobJobActivity1

 ## 참고
 Durable Function란? https://learn.microsoft.com/ko-kr/azure/azure-functions/durable/durable-functions-overview?tabs=csharp