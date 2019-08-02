using System;

namespace UrlShortener.Models
{
    public class GetUrlStatsResponse
    {
        public DateTime Created_at { get; set; }
        public DateTime? Last_usage { get; set; }
        public int Usage_count { get; set; }
    }
}