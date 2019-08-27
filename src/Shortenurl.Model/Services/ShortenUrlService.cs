using shortenurl.model.DTOs;
using shortenurl.model.Exceptions;
using shortenurl.model.Interfaces.Repositories;
using shortenurl.model.Interfaces.Services;
using shortenurl.model.ViewModels;
using System;
using System.Threading.Tasks;

namespace shortenurl.model.Services
{
    public class ShortenUrlService : IShortenUrlService
    {
        private readonly IShortenUrlRepository _shortenUrlRepository;
        private readonly ICodeService _codeService;
        public ShortenUrlService(IShortenUrlRepository shortenUrlRepository, ICodeService codeService)
        {
            _shortenUrlRepository = shortenUrlRepository;
            _codeService = codeService;
        }

        public async Task<ShortUrlCreatedViewModel> CreateShortenUrl(ShortenUrlDTO shortenUrlDTO)
        {
            if (string.IsNullOrEmpty(shortenUrlDTO.Code))
            {
                shortenUrlDTO.Code = _codeService.GenerateCode(6, new Random());
            }

            if (_codeService.IsCodeValid(shortenUrlDTO.Code))
            {

                var shortenUrl = await _shortenUrlRepository.GetShortenUrl(shortenUrlDTO.Code);

                if (shortenUrl != null)
                {
                    throw new ConflictException("Code in Use");
                }


                await _shortenUrlRepository.InsertShortenUrl(shortenUrlDTO);
                return new ShortUrlCreatedViewModel { Code = shortenUrlDTO.Code };
            }
            else
            {
                throw new UnprocessableEntityException("Code should be alphanumeric and 6 chars long");
            }

        }

        public async Task<string> GetUrlByCode(string code)
        {
            var shortenUrl = await _shortenUrlRepository.GetShortenUrl(code);

            if (shortenUrl != null)
            {
                await _shortenUrlRepository.UpdateUsage(shortenUrl.ShortUrlId);
                return shortenUrl.OriginalUrl;
            }
            else
                throw new NotFoundException("Code Not Found");
        }

        public async Task<UrlStatsViewModel> GetStatsByCode(string code)
        {
            var shortenUrl = await _shortenUrlRepository.GetShortenUrl(code);

            if (shortenUrl != null)
            {
                return new UrlStatsViewModel { CreatedAt = shortenUrl.CreatedAt, LastUsage = shortenUrl.LastUsage, UsageCount = shortenUrl.UsageCount };
            }
            else
                throw new NotFoundException("Code Not Found");
        }
    }
}
