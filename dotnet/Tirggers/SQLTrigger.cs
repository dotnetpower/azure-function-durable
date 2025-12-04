using System.Collections.Generic;
using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Logging;
using Microsoft.Azure.WebJobs.Extensions.Sql;
using Microsoft.Function.Triggers.Models;

namespace Microsoft.Function.Triggers
{
    //참고: https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-azure-sql-trigger?tabs=in-process%2Cportal&pivots=programming-language-csharp

    /* 중요
        DB 변경 추적을 위해서 다음 명령 필수. 
        
        ALTER DATABASE [your database name]
        SET CHANGE_TRACKING = ON
        (CHANGE_RETENTION = 2 DAYS, AUTO_CLEANUP = ON);

        ALTER TABLE [dbo].[your table name]
        ENABLE CHANGE_TRACKING;
    */
    public static class ToDoTrigger
    {
        [FunctionName("ToDoTrigger")]
        public static void Run(
            [SqlTrigger("[dbo].[ToDo]", ConnectionStringSetting = "SqlConnectionString")]
            IReadOnlyList<SqlChange<ToDoItem>> changes,
            ILogger logger)
        {
            // 보안: 변경된 데이터의 개수만 로그에 기록 (민감한 데이터 보호)
            logger.LogInformation("SQL Trigger processed {ChangeCount} change(s).", changes.Count);
        }
    }
}