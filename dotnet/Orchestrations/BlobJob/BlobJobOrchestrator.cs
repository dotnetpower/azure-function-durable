

using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Azure.EventHubs;
using System.Text;
using System.Net.Http;
using Microsoft.Extensions.Logging;
using Microsoft.Azure.WebJobs.Extensions.DurableTask;
using System.Threading.Tasks;
using Microsoft.Function.Orchestrations.Activities;

namespace Microsoft.Function.Orchestrations.BlobJob
{
    public class BlobJobOrchestrator
    {
        
        //BlobJobOrchestrator 는 Orchestratior 로써 IoTHub_Trigger 가 호출한다.
        [FunctionName(nameof(BlobJobOrchestrator))]
        public async Task Run(
            [OrchestrationTrigger]IDurableOrchestrationContext context,
            ILogger log)
        {
            var message = context.GetInput<string>();
            log.LogInformation($"BlobJobOrchestrator processed a message: {message}");

            //Activity 이름
            string BlobJobActivity = nameof(BlobJobActivity1);

            var result = await context.CallActivityAsync<string>(
                BlobJobActivity,
                message);


            //Orchestrator 인스턴스 ID
            log.LogInformation($"activity result: '{result}'");

        }
    }
}