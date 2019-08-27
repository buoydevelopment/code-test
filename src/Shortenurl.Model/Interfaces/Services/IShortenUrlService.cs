using shortenurl.model.DTOs;
using shortenurl.model.ViewModels;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace shortenurl.model.Interfaces.Services
{
    public interface IShortenUrlService
    {
        Task<ShortUrlCreatedViewModel> CreateShortenUrl(ShortenUrlDTO shortenUrlDTO);

        Task<string> GetUrlByCode(string code);


        Task<UrlStatsViewModel> GetStatsByCode(string code);
    }
}
