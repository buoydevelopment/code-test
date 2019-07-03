using System;

namespace UrlShortener.Entities
{
    public class UrlData
    {
        public string Code { get; set; }
        public string URL { get; set; }
        public System.DateTime Start_Date { get; set; }
        public Nullable<System.DateTime> Last_Usage { get; set; }
        public int Usage_Count { get; set; }
    }
}