using System.Threading.Tasks;
using Microsoft.Azure.EventHubs;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.DurableTask;
using Microsoft.Extensions.Logging;

namespace Microsoft.Function.Orchestrations.Activities
{
    public class BlobJobActivity1
    {
        [FunctionName(nameof(BlobJobActivity1))]
        public async Task<string> Run(
            [ActivityTrigger]IDurableActivityContext activityContext,            
            ILogger log)
        {

            var message = activityContext.GetInput<string>();

            string result = $"BlobJobActivity1: {message}";
            
            return await Task.FromResult(result);

        }
    }

    
}