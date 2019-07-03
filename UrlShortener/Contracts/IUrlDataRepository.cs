using System;
using UrlShortener.Models;

namespace UrlShortener.Contracts
{
    public interface IUrlDataRepository
    {
        bool PostNewUrl(PostNewUrlRequest request, string code);
        Uri GetUrl(string code);
        GetUrlStatsResponse GetUrlStats(string code);
    }
}