using System;

namespace UrlShortener.CrossCutting.Exceptions
{
    public class UnprocessableEntityException : Exception
    {
        public UnprocessableEntityException()
        {
        }

        public UnprocessableEntityException(string message) : base(message)
        {
        }

        public UnprocessableEntityException(string message, Exception inner)
        : base(message, inner)
        {
        }
    }
}
