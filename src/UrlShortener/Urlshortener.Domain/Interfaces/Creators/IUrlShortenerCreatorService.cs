using System;
using System.Collections.Generic;
using System.Text;
using UrlShortener.Domain.Dto;
using UrlShortener.Domain.Entities;

namespace UrlShortener.Domain.Interfaces.Creators
{
    public interface IUrlShortenerCreatorService
    {
        ShortUrl Execute(ShortUrlDto shortUrlDto);
    }
}
