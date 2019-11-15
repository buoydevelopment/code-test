using AutoMapper;
using UrlShortener.Domain.Dto;
using UrlShortener.Domain.Entities;

namespace UrlShortener.Api.Bootstrap
{
    public class MappingProfile : Profile
    {
        public MappingProfile()
        {
            CreateMap<ShortUrlDto, ShortUrl>();
            CreateMap<ShortUrl, ShortUrlDto>();

            CreateMap<ShortUrl, UrlStatDto>();
        }
    }
}
