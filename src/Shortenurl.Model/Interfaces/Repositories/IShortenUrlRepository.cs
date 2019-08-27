using shortenurl.model.DTOs;
using shortenurl.model.Entities;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace shortenurl.model.Interfaces.Repositories
{
    public interface IShortenUrlRepository
    {
        Task<ShortenUrl> GetShortenUrl(string Code);

        Task InsertShortenUrl(ShortenUrlDTO shortenUrlDTO);

        Task UpdateUsage(int shortUrlId);

    }
}
