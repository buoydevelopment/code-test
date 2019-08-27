using shortenurl.model.DTOs;
using shortenurl.model.Entities;
using shortenurl.model.Interfaces;
using shortenurl.model.Interfaces.Repositories;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace shortenurl.model.Repositories
{
    public class ShortenUrlRepository : IShortenUrlRepository
    {

        private readonly ISqlDataAccess _sqlDataAccess;
        public ShortenUrlRepository(ISqlDataAccess sqlDataAccess)
        {
            _sqlDataAccess = sqlDataAccess;
        }

        public async Task<ShortenUrl> GetShortenUrl(string code)
        {
            var parameters = new Dictionary<string, object>
            {
                { "Code", code },
            };
           return await _sqlDataAccess.GetOne<ShortenUrl>("uspGetShortUrl", parameters);
        }

        public async Task InsertShortenUrl(ShortenUrlDTO shortenUrlDTO)
        {
            var parameters = new Dictionary<string, object>
            {
                { "Code", shortenUrlDTO.Code },
                { "OriginalUrl", shortenUrlDTO.Url }
            };

            await _sqlDataAccess.Execute("uspInsertShortUrl", parameters);
        }

        public async Task UpdateUsage(int shortUrlId)
        {
            var parameters = new Dictionary<string, object>
            {
                { "ShortUrlId", shortUrlId },
            };
            await _sqlDataAccess.Execute("uspUpdateUsage", parameters);
        }
    }
}
