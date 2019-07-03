using Microsoft.AspNetCore.Mvc;

namespace UrlShortener.Controllers
{
    public partial class UrlsController
    {
        [Route("api/{code}/stats")]
        [HttpGet]
        public IActionResult GetUrlStats(string code)
        {
            var response = urlDataRepository.GetUrlStats(code);

            if (response == null)
                return NotFound();

            return Ok(response);
        }
    }
}