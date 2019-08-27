using System;
using System.Collections.Generic;
using System.Text;

namespace shortenurl.model.ViewModels
{
    public class UrlStatsViewModel
    {
        public DateTime CreatedAt { get; set; }

        public DateTime? LastUsage { get; set; }

        public int UsageCount { get; set; }
    }
}
