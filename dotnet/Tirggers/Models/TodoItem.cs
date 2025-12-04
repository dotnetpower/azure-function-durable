using System;

namespace Microsoft.Function.Triggers.Models
{
    // SQLTrigger 함수에서 Model 로 사용됨
    public class ToDoItem
    {
        public Guid Id { get; set; }
        public int? order { get; set; }
        public string title { get; set; }
        public string url { get; set; }
        public bool? completed { get; set; }
    }
}