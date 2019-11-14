﻿using System;

namespace UrlShortener.CrossCutting.Exceptions
{
    public class ConflictException : Exception
    {
        public ConflictException()
        {
        }

        public ConflictException(string message) : base(message)
        {
        }

        public ConflictException(string message, Exception inner)
        : base(message, inner)
        {
        }
    }
}
