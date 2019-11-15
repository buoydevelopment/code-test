using System;

namespace UrlShortener.Domain.Entities
{
    public class ShortUrl : BaseEntity
    {
        public string Code { get; set; }

        public string Url { get; set; }

        public DateTime CreatedAt { get; set; }

        public DateTime? LastUsage { get; set; }

        public int UsageCount { get; set; }
    }
}
