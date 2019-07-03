using Microsoft.AspNetCore.Mvc;
using System;
using System.Text.RegularExpressions;
using UrlShortener.Entities;
using UrlShortener.Models;

namespace UrlShortener.Controllers
{
    public partial class UrlsController
    {
        [Route("api/urls")]
        [HttpPost]
        public IActionResult PostNewUrl([FromBody] PostNewUrlRequest request)
        {
            if (string.IsNullOrEmpty(request.Url))
            {
                return BadRequest();
            }

            var code = request.Code;

            var regexItem = new Regex("^[a-zA-Z0-9]*$");
            if (!String.IsNullOrEmpty(code) && (code.Length != 6 || !regexItem.IsMatch(code)))
            {
                //Unprocessable entity
                return UnprocessableEntity();
            }

            if (String.IsNullOrEmpty(request.Code))
                code = CodeGenerator.GetShortCode(request);

            var response = urlDataRepository.PostNewUrl(request, code);

            if (!response)
                return Conflict();

            return Created("DefaultApi", new PostNewUrlResponse(code));
        }
    }
}