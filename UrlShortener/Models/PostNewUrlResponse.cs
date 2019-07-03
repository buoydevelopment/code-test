namespace UrlShortener.Models
{
    public class PostNewUrlResponse
    {
        public string Code { get; set; }

        public PostNewUrlResponse(string code)
        {
            this.Code = code;
        }
    }
}