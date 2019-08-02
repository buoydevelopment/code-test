using Microsoft.AspNetCore.Mvc;
using UrlShortener.Contracts;

namespace UrlShortener.Controllers
{
    //[Route("api/[controller]")]
    [ApiController]
    public partial class UrlsController : Controller
    {
        private readonly IUrlDataRepository urlDataRepository;

        public UrlsController(IUrlDataRepository urlDataRepository)
        {
            this.urlDataRepository = urlDataRepository;
        }
    }
}