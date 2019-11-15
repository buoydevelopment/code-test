using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using UrlShortener.Domain.Dto;
using UrlShortener.Domain.Entities;

namespace UrlShortener.Domain.Interfaces
{
    public interface IUrlShortenerService
    {
        ShortUrCreatedlDto Add(ShortUrlDto shortUrl);

        Task<string> GetUrlByCode(string code);

        Task<UrlStatDto> GetStatByCode(string code);
    }
}
