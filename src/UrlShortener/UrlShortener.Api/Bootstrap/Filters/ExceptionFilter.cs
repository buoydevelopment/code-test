using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

namespace UrlShortener.Api.Bootstrap.Filters
{
    public class ExceptionFilter : ExceptionFilterAttribute
    {
        public override void OnException(ExceptionContext context)
        {
            var message = context.Exception.GetBaseException().Message;

            var exceptionName = context.Exception.GetType().Name;

            var exception = ExceptionFilterFactory.Get(exceptionName);

            context.HttpContext.Response.StatusCode = exception;

            context.Result = new JsonResult(message);

            base.OnException(context);
        }
    }
}
