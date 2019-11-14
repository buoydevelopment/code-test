using System;
using System.Collections.Generic;
using System.Text;

namespace UrlShortener.Domain.Interfaces.Commands
{
    public interface IGenerateCodeCommand : ICommandWithResult<int, string>
    {
    }
}
