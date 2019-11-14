using System;
using UrlShortener.Domain.Entities;
using UrlShortener.Domain.Interfaces.Commands;

namespace UrlShortener.Domain.Commands
{
    public class ShortenUrlUsageCommand : IShortenUrlUsageCommand
    {
        public ShortUrl Execute(ShortUrl entity)
        {
            entity.LastUsage = DateTime.Now;
            entity.UsageCount = ++entity.UsageCount;

            return entity;
        }
    }
}
