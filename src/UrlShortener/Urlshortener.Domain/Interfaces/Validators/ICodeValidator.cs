using System;
using System.Collections.Generic;
using System.Text;

namespace UrlShortener.Domain.Interfaces.Validators
{
    public interface ICodeValidator : ICommandWithResult<string, bool>
    {
    }
}
