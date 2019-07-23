using System;

namespace Test.Dto
{
    public class UrlDto
    {
        public string SourceUrl { get; set; }
        public string TargetUrl { get; set; }
        public bool Valid { get; set; }
        public string Code { get; set; }
        public int Usage_Count { get; set; }
    }

    public class SourceUrlDto
    {
        public string Url { get; set; }
    }
    }
