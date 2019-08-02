using System.Collections.Generic;

namespace UrlShortener.Entities
{
    public class UrlDataList
    {
        public List<UrlData> UrlList { get; set; }

        public UrlDataList()
        {
            this.UrlList = new List<UrlData>();
        }
    }
}