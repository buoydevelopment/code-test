using System;
using System.Collections.Generic;
using System.Text;

namespace shortenurl.model.Exceptions
{
    public class UnprocessableEntityException: Exception
    {
        public UnprocessableEntityException(string message) : base(message)
        {

        }
    }
}
