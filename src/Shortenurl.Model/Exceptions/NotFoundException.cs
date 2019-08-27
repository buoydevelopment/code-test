using System;
using System.Collections.Generic;
using System.Text;

namespace shortenurl.model.Exceptions
{
    public class NotFoundException: Exception
    {
        public NotFoundException(string message) : base(message)
        {

        }
    }
}
