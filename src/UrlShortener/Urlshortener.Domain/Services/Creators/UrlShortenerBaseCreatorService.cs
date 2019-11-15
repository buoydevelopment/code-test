using AutoMapper;
using UrlShortener.Domain.Dto;
using UrlShortener.Domain.Entities;
using UrlShortener.Domain.Interfaces.Creators;

namespace UrlShortener.Domain.Services.UrlShortenerCreatorService
{
    public abstract class UrlShortenerBaseCreatorService : IUrlShortenerCreatorService
    {
        private readonly IMapper mapper;

        public UrlShortenerBaseCreatorService(IMapper mapper)
        {
            this.mapper = mapper;
        }

        protected abstract bool IsValid(string code);
        protected abstract void UnprocessableEntity();
        protected abstract bool IsConflictEntity(string code);
        protected abstract void ConflictEntity(string code);

        public ShortUrl Execute(ShortUrlDto shortUrlDto)
        { 
            if (!IsValid(shortUrlDto.Code))
            {
                UnprocessableEntity();
            }

            if (IsConflictEntity(shortUrlDto.Code))
            {
                ConflictEntity(shortUrlDto.Code);
            }

            return this.mapper.Map<ShortUrl>(shortUrlDto);
        }
    }
}
