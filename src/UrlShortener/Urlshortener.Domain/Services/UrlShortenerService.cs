using AutoMapper;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using UrlShortener.CrossCutting.Exceptions;
using UrlShortener.Domain.Dto;
using UrlShortener.Domain.Entities;
using UrlShortener.Domain.Interfaces;
using UrlShortener.Domain.Interfaces.Commands;
using UrlShortener.Domain.Interfaces.Creators;

namespace UrlShortener.Domain.Services
{
    public class UrlShortenerService : IUrlShortenerService
    {
        private readonly IRepository<ShortUrl> repository;
        private readonly IGenerateCodeCommand generateCodeCommand;
        private readonly IMapper mapper;
        private readonly IUrlShortenerCreatorService urlShortenerCreatorService;
        private readonly IShortenUrlUsageCommand shortenUrlUsageCommand;

        private static int length = 6;

        public UrlShortenerService(IRepository<ShortUrl> repository,
            IGenerateCodeCommand generateCodeCommand,
            IUrlShortenerCreatorService urlShortenerCreatorService,
            IShortenUrlUsageCommand shortenUrlUsageCommand,
            IMapper mapper)
        {
            this.repository = repository;
            this.generateCodeCommand = generateCodeCommand;
            this.mapper = mapper;
            this.urlShortenerCreatorService = urlShortenerCreatorService;
            this.shortenUrlUsageCommand = shortenUrlUsageCommand;
        }

        public ShortUrCreatedlDto Add(ShortUrlDto shortUrlDto)
        {
            var shortUrl = CreateShortenUrl(shortUrlDto);

            this.repository.Add(shortUrl);

            return new ShortUrCreatedlDto { Code = shortUrl.Code} ;
        }

        public async Task<string> GetUrlByCode(string code)
        {
            var query = await this.repository.ListAsync(x => x.Code.Equals(code));

            var entity = GetEntityByCode(query, code);

            entity = this.shortenUrlUsageCommand.Execute(entity);

            this.repository.Update(entity);

            return entity.Url;
      }

        public async Task<UrlStatDto> GetStatByCode(string code)
        {
            var query = await this.repository.ListAsync(x => x.Code.Equals(code));

            var entity = GetEntityByCode(query, code);

            return this.mapper.Map<UrlStatDto>(entity);
        }

        private ShortUrl GetEntityByCode(IList<ShortUrl> query, string code)
        {
            var entity = query.FirstOrDefault();

            if (entity == null)
            {
                throw new NotFoundException($"The Code [{code}] cannot be found");
            }

            return entity;
        }

        private ShortUrl CreateShortenUrl(ShortUrlDto shortUrlDto)
        {
            if (string.IsNullOrEmpty(shortUrlDto.Code))
            {
                shortUrlDto.Code = GenerateCode();
            }

            var shortUrlEntity = urlShortenerCreatorService.Execute(shortUrlDto);

            return shortUrlEntity;
        }
        
        private string GenerateCode() => this.generateCodeCommand.Execute(length);
    }
}
