using System;
using System.Collections.Generic;
using System.Text;
using UrlShortener.Domain.Entities;

namespace UrlShortener.Domain.Interfaces.Commands
{
    public interface IShortenUrlUsageCommand : ICommandWithResult<ShortUrl, ShortUrl>
    {
    }
}
