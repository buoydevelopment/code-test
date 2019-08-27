using System;
using System.Collections.Generic;
using System.Text;

namespace shortenurl.model.Entities
{
    public class ShortenUrl
    {
        public int ShortUrlId { get; set; }

        public string Code { get; set; }

        public string OriginalUrl { get; set; }

        public DateTime CreatedAt { get; set; }

        public DateTime LastUsage { get; set; }

        public int UsageCount { get; set; }
        

    }
}
