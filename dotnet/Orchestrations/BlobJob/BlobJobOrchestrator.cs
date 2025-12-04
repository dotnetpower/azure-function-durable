

using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Azure.EventHubs;
using System.Text;
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
            
            // 보안: Orchestrator에서는 ReplaySafeLogger를 사용해야 하며, 민감한 데이터는 로그에 기록하지 않음
            if (!context.IsReplaying)
            {
                log.LogInformation("BlobJobOrchestrator processing message. InstanceId: {InstanceId}", context.InstanceId);
            }

            //Activity 이름
            string BlobJobActivity = nameof(BlobJobActivity1);

            var result = await context.CallActivityAsync<string>(
                BlobJobActivity,
                message);


            //Orchestrator 인스턴스 ID
            if (!context.IsReplaying)
            {
                log.LogInformation("Activity completed for InstanceId: {InstanceId}", context.InstanceId);
            }

        }
    }
}