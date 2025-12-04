using IoTHubTrigger = Microsoft.Azure.WebJobs.EventHubTriggerAttribute;

using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Azure.EventHubs;
using System.Text;
using System.Net.Http;
using Microsoft.Extensions.Logging;
using Microsoft.Azure.WebJobs.Extensions.DurableTask;
using System.Threading.Tasks;
using Microsoft.Function.Orchestrations.BlobJob;

namespace Microsoft.Function.Triggers
{
    public class IoTHub_Trigger
    {
        private static HttpClient client = new HttpClient();
        
        //IoTHub_Tirgger 는 Connection에 정의된 Endpoint의 IoT Hub 에서 이벤트가 발생하면 실행되며, 이 트리거 함수 자체가 오케스트레이션 클라이언트가 됨
        [FunctionName("IoTHub_Trigger")]
        public async Task Run(
            [IoTHubTrigger("messages/events", Connection = "IoTHubConnectionString")]EventData message, 
            [DurableClient]IDurableClient orchestratorClient,
            ILogger log)
        {

            var strMessage = Encoding.UTF8.GetString(message.Body.Array);

            log.LogInformation($"C# IoT Hub trigger function processed a message: {strMessage}");

            //Orchestrator 이름
            //var orchestratorName = "BlobJobOrchestrator";
            var orchestratorName = nameof(BlobJobOrchestrator); //Function 이름이 변경될수도 있으므로 nameof를 사용한다.

            //전달 할 파라메타
            var orchestratorInput = strMessage;

            //Orchestrator 이름 다음에 instanceid 파라메타가 오버라이드 되어 있으므로, 생략하려면 Input 값의 타입을 명시적으로 선언 필요.
            var instanceId = await orchestratorClient.StartNewAsync<string>(
                    orchestratorName,
                    orchestratorInput);

            //Orchestrator 인스턴스 ID
            log.LogInformation($"Started Orchestrator with ID = '{instanceId}'...");

        }
    }
}