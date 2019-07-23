using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace Test.Data.Entities
{
    public class Url : EntityBase
    {
      
        public string SourceUrl { get; set; }
        public string TargetUrl { get; set; }
        public bool Valid { get; set; }
        public string Code { get; set; }
        public int Usage_Count { get; set; }
    }
}
