using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Test.Dto;
using Test.Service.Interfaces;
using Test.Service.Services;

// For more information on enabling MVC for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace Test.Web.API.Controllers
{

    [Route("api/Url")]
    [ApiController]
    [Produces("application/json")]
    public class UrlController : ControllerBase
    {

        private readonly IUrlService _urlService;

        public UrlController(IUrlService urlService)
        {
            _urlService = urlService;
        }

        #region model
       

        [HttpGet]
        [Route("GetUrlByCode")]
        public async Task<IActionResult> GetUrlByCode(string Code)
        {

            try
            {

                var result = await _urlService.GetUrl(Code);
                if (result == null)
                {
                    return this.NotFound();
                }

                return this.Redirect(result.SourceUrl);

               
            }
            catch (Exception ex)
            {
               
                return BadRequest(new { message = ex.Message });
            }

        }
    


        [HttpPost]
        [Route("Create")]
        public async Task<IActionResult> Create(SourceUrlDto model)
        {

            try
            {
                var result = await _urlService.CreateShortCode(model);

                if (!result.IsSuccess)
                {
                    return BadRequest(result);
                }

                return Ok(result.Response);


            }
            catch (Exception ex)
            {
                
                return BadRequest(new { message = ex.Message });
            }

        }
       


        #endregion

    }
}
