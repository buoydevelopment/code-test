using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;
using UrlShortener.Domain.Dto;
using UrlShortener.Domain.Interfaces;

namespace UrlShortener.Api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ShortUrlController : ControllerBase
    {
        private readonly IUrlShortenerService urlShortenerService;
        public ShortUrlController(IUrlShortenerService urlShortenerService)
        {
            this.urlShortenerService = urlShortenerService;
        }

        [HttpPost]
        public IActionResult Post(ShortUrlDto shortUrlDto)
        {
            if (string.IsNullOrEmpty(shortUrlDto.Url))
            {
                return BadRequest("Url is not present");
            }

            var shortUrlCreated = this.urlShortenerService.Add(shortUrlDto);

            return Created(string.Empty, shortUrlCreated);
        }

        [HttpGet("{code}/stats")]
        public async Task<IActionResult> GetStatByCode(string code)
        {   
            var result = await this.urlShortenerService.GetStatByCode(code);
            
            return Ok(result);
        }

        [HttpGet("{code}")]
        public async Task<IActionResult> GetUrlByCode(string code)
        {
            var url = await this.urlShortenerService.GetUrlByCode(code);

            return Redirect(url);
        }
    }
}