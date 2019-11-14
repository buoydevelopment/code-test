using AutoMapper;
using Moq;
using System;
using System.Collections.Generic;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;
using UrlShortener.CrossCutting.Exceptions;
using UrlShortener.Domain.Commands;
using UrlShortener.Domain.Dto;
using UrlShortener.Domain.Entities;
using UrlShortener.Domain.Interfaces;
using UrlShortener.Domain.Interfaces.Creators;
using UrlShortener.Domain.Services;
using Xunit;

namespace UrlShortener.Test.Services
{
    public class UrlShortenerServiceTest
    {
        private readonly Mock<IMapper> mapper;
        private readonly Mock<IRepository<ShortUrl>> repository;
        private readonly new Mock<IUrlShortenerCreatorService> creatorService;

        public UrlShortenerServiceTest()
        {
            this.mapper = new Mock<IMapper>();
            this.repository = new Mock<IRepository<ShortUrl>>();
            this.creatorService = new Mock<IUrlShortenerCreatorService>();

            this.mapper.Setup(x => x.Map<ShortUrl>(It.IsAny<ShortUrlDto>()));
        }

        [Fact]
        public void ShouldAddNewShortUrlEntity()
        {
            var urlShortenDto = new ShortUrlDto
            {
                Code = "Code1",
                Url = "www.example.com"
            };

            var urlShorten = new ShortUrl
            {
                Code = "Code1",
                Url = "www.example.com"
            };       

            creatorService.Setup(x => x.Execute(urlShortenDto))
                          .Returns(urlShorten);

            var service = new UrlShortenerService(repository.Object,
                                                  new GenerateCodeCommand(),
                                                  creatorService.Object,
                                                  new ShortenUrlUsageCommand(),
                                                  mapper.Object);
        

            var result = service.Add(urlShortenDto);

            repository.Verify(x => x.Add(It.IsAny<ShortUrl>()), Times.Once);
            Assert.Equal(urlShortenDto.Code, result.Code);
        }

        [Fact]
        public void ShouldAddNewShortUrlEntityFromEmptyCode()
        {
            var urlShortenDto = new ShortUrlDto
            {
                Url = "www.example.com"
            };

            var urlShorten = new ShortUrl
            {
                Code = "Code1",
                Url = "www.example.com"
            };

            creatorService.Setup(x => x.Execute(urlShortenDto))
                          .Returns(urlShorten);

            var service = new UrlShortenerService(repository.Object,
                                                  new GenerateCodeCommand(),
                                                  creatorService.Object,
                                                  new ShortenUrlUsageCommand(),
                                                  mapper.Object);


            var result = service.Add(urlShortenDto);

            repository.Verify(x => x.Add(It.IsAny<ShortUrl>()), Times.Once);
            
            Assert.False(string.IsNullOrEmpty(result.Code));
            Assert.False(string.IsNullOrEmpty(urlShortenDto.Code));
        }

        [Fact]
        public void ShouldReturnShortUrlEntityFromCodeAndUpdate()
        {
            var code = "Code1";

            var urlShortenDto = new ShortUrlDto
            {
                Code = "Code1",
                Url = "www.example.com"
            };

            var urlShorten = new ShortUrl
            {
                Code = "Code1",
                Url = "www.example.com"
            };

            creatorService.Setup(x => x.Execute(urlShortenDto))
                          .Returns(urlShorten);

            var list = new List<ShortUrl>
            { 
                new ShortUrl { Code = "Code2", Url = "www.example2.com" }
            };

            var task = Task.FromResult<IList<ShortUrl>>(list);

            repository.Setup(x => x.ListAsync(It.IsAny<Expression<Func<ShortUrl, bool>>>()))
                      .Returns(task);

            var service = new UrlShortenerService(repository.Object,
                                                  new GenerateCodeCommand(),
                                                  creatorService.Object,
                                                  new ShortenUrlUsageCommand(),
                                                  mapper.Object);


            var result = service.GetUrlByCode(code).Result;

            repository.Verify(x => x.ListAsync(It.IsAny<Expression<Func<ShortUrl, bool>>>()), Times.Once);
            repository.Verify(x => x.Update(It.IsAny<ShortUrl>()), Times.Once);

            Assert.False(string.IsNullOrEmpty(result));
        }

        [Fact]
        public void ShouldThrowExceptionWhenNotFoundAEntityByCode()
        {
            var code = "Code1";

            var urlShortenDto = new ShortUrlDto
            {
                Code = "Code1",
                Url = "www.example.com"
            };

            var urlShorten = new ShortUrl
            {
                Code = "Code1",
                Url = "www.example.com"
            };

            creatorService.Setup(x => x.Execute(urlShortenDto))
                          .Returns(urlShorten);

            var list = new List<ShortUrl>();

            var task = Task.FromResult<IList<ShortUrl>>(list);

            repository.Setup(x => x.ListAsync(It.IsAny<Expression<Func<ShortUrl, bool>>>()))
                      .Returns(task);

            var service = new UrlShortenerService(repository.Object,
                                                  new GenerateCodeCommand(),
                                                  creatorService.Object,
                                                  new ShortenUrlUsageCommand(),
                                                  mapper.Object);

            Assert.ThrowsAsync<NotFoundException>(() => service.GetUrlByCode(code));
        }

        [Fact]
        public void ShoulReturnStatsByCode()
        {
            var code = "Code1";

            var statDto = new UrlStatDto
            {
                CreatedAt = DateTime.Now.AddDays(-2),
                LastUsage = DateTime.Now,
                UsageCount = 1
            };

            var urlShortenDto = new ShortUrlDto
            {
                Code = "Code1",
                Url = "www.example.com"
            };

            var urlShorten = new ShortUrl
            {
                Code = "Code1",
                Url = "www.example.com"
            };

            this.mapper.Setup(x => x.Map<UrlStatDto>(urlShorten))
                       .Returns(statDto);

            creatorService.Setup(x => x.Execute(urlShortenDto))
                          .Returns(urlShorten);

            var list = new List<ShortUrl> { urlShorten };

            var task = Task.FromResult<IList<ShortUrl>>(list);

            repository.Setup(x => x.ListAsync(It.IsAny<Expression<Func<ShortUrl, bool>>>()))
                      .Returns(task);

            var service = new UrlShortenerService(repository.Object,
                                                  new GenerateCodeCommand(),
                                                  creatorService.Object,
                                                  new ShortenUrlUsageCommand(),
                                                  mapper.Object);

            var result = Task.Run(() => service.GetStatByCode(code)).Result;

            repository.Verify(x => x.ListAsync(It.IsAny<Expression<Func<ShortUrl, bool>>>()), Times.Once);
            Assert.Equal(1, result.UsageCount);
            Assert.True(DateTime.Now > result.CreatedAt);
            Assert.True(result.UsageCount > 0);
        }
    }
}
