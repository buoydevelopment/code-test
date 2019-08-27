using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using shortenurl.model.Exceptions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;

namespace shortenurl.api.Filters
{
    public class CustomExceptionFilter : ExceptionFilterAttribute
    {
        public override void OnException(ExceptionContext context)
        {
            var msg = context.Exception.GetBaseException().Message;
            string stack = context.Exception.StackTrace;

            switch (context.Exception.GetType().Name)
            {
                case "NotFoundException":
                    context.HttpContext.Response.StatusCode = (int)HttpStatusCode.NotFound;
                    break;
                case "UnprocessableEntityException":
                    context.HttpContext.Response.StatusCode = (int)HttpStatusCode.UnprocessableEntity;
                    break;
                case "ConflictException":
                    context.HttpContext.Response.StatusCode = (int)HttpStatusCode.Conflict;
                    break;
                default:
                    context.HttpContext.Response.StatusCode = (int)HttpStatusCode.InternalServerError;
                    break;
            }

            context.Result = new JsonResult(msg);
            base.OnException(context);
        }
    }
}
