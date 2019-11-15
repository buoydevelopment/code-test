using System;
using System.Text.Json.Serialization;

namespace UrlShortener.Domain.Dto
{
    public class UrlStatDto
    {
        [JsonIgnore]
        public DateTime CreatedAt { get; set; }

        [JsonIgnore]
        public DateTime? LastUsage { get; set; }

        public int UsageCount { get; set; }

        [JsonPropertyName("CreatedAt")]
        public string CreatedAtUTC
        { 
            get
            { 
                return CreatedAt.ToUniversalTime().ToString("yyyy'-'MM'-'dd'T'HH':'mm':'ssZ");
            } 
        }

        [JsonPropertyName("LastUsage")]
        public string LastUsageUTC
        {
            get
            { 
                return LastUsage != null ? LastUsage.Value.ToUniversalTime().ToString("yyyy'-'MM'-'dd'T'HH':'mm':'ssZ") : null;
            }
        }
    }
}
