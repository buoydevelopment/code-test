using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using shortenurl.model.DTOs;
using shortenurl.model.Interfaces.Services;
using shortenurl.model.ViewModels;

namespace shortenurl.api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ShortenUrlController : ControllerBase
    {
        
        [HttpPost]
        [Route("urls")]
        public async Task<ActionResult<ShortUrlCreatedViewModel>> CreateShortenUrl(ShortenUrlDTO shortenUrlDTO,[FromServices]IShortenUrlService shortenUrlService)
        {

           var code = await shortenUrlService.CreateShortenUrl(shortenUrlDTO);
           return Created(string.Empty,code);
        }

        [HttpGet("{code}")]
        public async Task<IActionResult> Get(string code, [FromServices]IShortenUrlService shortenUrlService)
        {
            var location = await shortenUrlService.GetUrlByCode(code);
            return Redirect(location);
        }


        [HttpGet("{code}/stats")]
        public async Task<ActionResult<UrlStatsViewModel>> GetCodeStats(string code, [FromServices]IShortenUrlService shortenUrlService)
        {
            var result = await shortenUrlService.GetStatsByCode(code);
            return Ok(result);
        }

    }
}
