using System;
using System.Collections.Generic;
using System.Net;

namespace UrlShortener.Api.Bootstrap.Filters
{
    public class ExceptionFilterFactory
    {
        private static IReadOnlyDictionary<string, int> Exceptions;

        static ExceptionFilterFactory()
        {
            Exceptions = new Dictionary<string, int>
            {
                {"BadRequestException" ,  (int)HttpStatusCode.BadRequest},
                {"ConflictException", (int)HttpStatusCode.Conflict},
                {"UnprocessableEntityException", (int)HttpStatusCode.UnprocessableEntity},
                {"NotFoundException", (int)HttpStatusCode.NotFound},
            };
        }

        public static int Get(string name)
        {
            int code;

            if (!Exceptions.TryGetValue(name, out code))
            {
                throw new ArgumentOutOfRangeException($"The name {name} is not mapped to any collection in the exception filter configuration");
            }

            return code;
        }
    }
}
