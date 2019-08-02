using Microsoft.AspNetCore.Mvc;
using System.Net;
using System.Net.Http;

namespace UrlShortener.Controllers
{
    public partial class UrlsController
    {
        [Route("api/{code}")]
        [HttpGet]
        public IActionResult GetUrl(string code)
        {
            var uri = urlDataRepository.GetUrl(code);
            if (uri == null)
                return NotFound();

            return Redirect(uri.ToString());
        }
    }
}