using AutoMapper;
using Moq;
using System;
using System.Collections.Generic;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;
using UrlShortener.CrossCutting.Exceptions;
using UrlShortener.Domain.Dto;
using UrlShortener.Domain.Entities;
using UrlShortener.Domain.Interfaces;
using UrlShortener.Domain.Interfaces.Validators;
using UrlShortener.Domain.Services.Creators;
using UrlShortener.Domain.Validators;
using Xunit;

namespace UrlShortener.Test.Services
{
    public class UrlShortenerCreatorServiceTest
    {
        private readonly ICodeValidator codeValidator;

        public UrlShortenerCreatorServiceTest()
        {
            this.codeValidator = new CodeValidator();
        }

        [Fact]
        public void ShouldGenerateUnprocessableEntityException()
        {
            var mapper = new Mock<IMapper>();
            mapper.Setup(x => x.Map<ShortUrl>(It.IsAny<ShortUrlDto>()));

            var repository = new Mock<IRepository<ShortUrl>>();

            var service = new UrlShortenerCreatorService(mapper.Object, 
                                                        repository.Object,
                                                        this.codeValidator);

            var shortenUrl = new ShortUrlDto
            {
                Code = "AAA",
                Url = "www.example.com"
            };

            Assert.Throws<UnprocessableEntityException>(() => service.Execute(shortenUrl));
        }

        [Fact]
        public void ShouldGenerateConflictException()
        {
            var shortenUrl = new ShortUrl
            {
                Code = "AAA123",
                Url = "www.example.com"
            };

            var mapper = new Mock<IMapper>();
            mapper.Setup(x => x.Map<ShortUrl>(It.IsAny<ShortUrlDto>()));

            var list = new List<ShortUrl> { shortenUrl };

            var task = Task.FromResult<IList<ShortUrl>>(list);

            var repository = new Mock<IRepository<ShortUrl>>();

            repository.Setup(x => x.ListAsync(It.IsAny<Expression<Func<ShortUrl, bool>>>()))
                      .Returns(task);

            var service = new UrlShortenerCreatorService(mapper.Object,
                                                        repository.Object,
                                                        this.codeValidator);

            var shortenUrlDto = new ShortUrlDto
            {
                Code = "AAA123",
                Url = "www.example.com"
            };

            Assert.Throws<ConflictException>(() => service.Execute(shortenUrlDto));
        }

        [Fact]
        public void ShouldReturnShortenUrlEntityFromDto()
        {
            var mapper = new Mock<IMapper>();
            mapper.Setup(x => x.Map<ShortUrl>(It.IsAny<ShortUrlDto>()))
                  .Returns(new ShortUrl
                  {
                    Code = "AAAZZ4",
                    Url = "www.example.com"
                  });

            var list = new List<ShortUrl>();

            var task = Task.FromResult<IList<ShortUrl>>(list);

            var repository = new Mock<IRepository<ShortUrl>>();

            repository.Setup(x => x.ListAsync(It.IsAny<Expression<Func<ShortUrl, bool>>>()))
                      .Returns(task);

            var service = new UrlShortenerCreatorService(mapper.Object,
                                                        repository.Object,
                                                        this.codeValidator);

            var shortenUrlDto = new ShortUrlDto
            {
                Code = "AAAZZ4",
                Url = "www.example.com"
            };

            var result = service.Execute(shortenUrlDto);

            Assert.Equal(result.Code, shortenUrlDto.Code);
            Assert.Equal(result.Url, shortenUrlDto.Url);
        }
    }
}
