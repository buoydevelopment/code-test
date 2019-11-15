using System.ComponentModel.DataAnnotations;

namespace UrlShortener.Domain.Dto
{
    public class ShortUrlDto
    {
        public string Code { get; set; }

        [Required]
        public string Url { get; set; }
    }
}
