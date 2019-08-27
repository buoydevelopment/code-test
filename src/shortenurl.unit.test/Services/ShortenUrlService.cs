using Moq;
using Newtonsoft.Json;
using shortenurl.model.DTOs;
using shortenurl.model.Entities;
using shortenurl.model.Exceptions;
using shortenurl.model.Interfaces.Repositories;
using shortenurl.model.Services;
using shortenurl.model.ViewModels;
using System;
using System.Threading.Tasks;
using Xunit;

namespace shortenurl.unit.test
{
    public class ShortenUrlServiceTest
    {
        [Theory]
        [InlineData("AbC123", "http://google.com")]
        [InlineData("", "http://google.com")]
        [InlineData(null, "http://google.com")]
        public async void CreateShortenUrlWithValidCodeOrEmpty(string code, string url)
        {
            var shortenUrlDTO = new ShortenUrlDTO { Code = code, Url = url };

            var ShortenUrlRepostory = new Mock<IShortenUrlRepository>();
            ShortenUrlRepostory.Setup(p => p.GetShortenUrl(It.IsAny<string>())).Returns(Task.FromResult<ShortenUrl>(null));
            ShortenUrlRepostory.Setup(p => p.InsertShortenUrl(It.IsAny<ShortenUrlDTO>()));

            var shortenUrlService = new ShortenUrlService(ShortenUrlRepostory.Object, new CodeService());

            var result = await shortenUrlService.CreateShortenUrl(shortenUrlDTO);

            if (string.IsNullOrEmpty(code))
            {
                Assert.NotEmpty(result.Code);
            }
            else
            {
                Assert.Equal(code, result.Code);
            }

            Assert.Equal(6, result.Code.Length);
        }



        [Theory]
        [InlineData("AbC12", "http://google.com")]
        [InlineData("AbC!23", "http://google.com")]
        public async void CreateShortenUrlInvalidCode(string code, string url)
        {
            var shortenUrlDTO = new ShortenUrlDTO { Code = code, Url = url };

            var ShortenUrlRepostory = new Mock<IShortenUrlRepository>();
            ShortenUrlRepostory.Setup(p => p.GetShortenUrl(It.IsAny<string>())).Returns(Task.FromResult<ShortenUrl>(null));
            ShortenUrlRepostory.Setup(p => p.InsertShortenUrl(It.IsAny<ShortenUrlDTO>()));

            var shortenUrlService = new ShortenUrlService(ShortenUrlRepostory.Object, new CodeService());


            await Assert.ThrowsAsync<UnprocessableEntityException>(() => shortenUrlService.CreateShortenUrl(shortenUrlDTO));

        }

        [Theory]
        [InlineData("AbC123", "http://google.com")]
        public async void CreateShortenUrlExistingCode(string code, string url)
        {
            var shortenUrlDTO = new ShortenUrlDTO { Code = code, Url = url };

            var ShortenUrlRepostory = new Mock<IShortenUrlRepository>();
            ShortenUrlRepostory.Setup(p => p.GetShortenUrl(It.IsAny<string>())).Returns(Task.FromResult<ShortenUrl>(new ShortenUrl()));
            ShortenUrlRepostory.Setup(p => p.InsertShortenUrl(It.IsAny<ShortenUrlDTO>()));

            var shortenUrlService = new ShortenUrlService(ShortenUrlRepostory.Object, new CodeService());


            await Assert.ThrowsAsync<ConflictException>(() => shortenUrlService.CreateShortenUrl(shortenUrlDTO));

        }

        [Fact]
        public async void GetUrlByCodeValid()
        {
            var code = "ABC123";
            var url = "http://google.com";

            var ShortenUrlRepostory = new Mock<IShortenUrlRepository>();
            ShortenUrlRepostory.Setup(p => p.GetShortenUrl(It.IsAny<string>())).Returns(Task.FromResult<ShortenUrl>(new ShortenUrl { Code = code, OriginalUrl = url }));
            var shortenUrlService = new ShortenUrlService(ShortenUrlRepostory.Object, new CodeService());

            var result = await shortenUrlService.GetUrlByCode(code);

            Assert.Equal(url, result);

        }


        [Fact]
        public async void GetUrlByCodeNotFound()
        {
            var code = "ABC123";

            var ShortenUrlRepostory = new Mock<IShortenUrlRepository>();
            ShortenUrlRepostory.Setup(p => p.GetShortenUrl(It.IsAny<string>())).Returns(Task.FromResult<ShortenUrl>(null));
            var shortenUrlService = new ShortenUrlService(ShortenUrlRepostory.Object, new CodeService());

            await Assert.ThrowsAsync<NotFoundException>(() => shortenUrlService.GetUrlByCode(code));
        }



        [Fact]
        public async void GetStatsByCodeValid()
        {
            var createdAt = DateTime.UtcNow.AddDays(-5);
            var lastUsage = DateTime.UtcNow;

            var shortenUrl = new ShortenUrl { Code = "ABC123", CreatedAt = createdAt, LastUsage = lastUsage, ShortUrlId = 1, OriginalUrl = "http://google.com", UsageCount = 3 };
            var expectedStats = new UrlStatsViewModel { CreatedAt = createdAt, LastUsage = lastUsage, UsageCount = 3 };

            var ShortenUrlRepostory = new Mock<IShortenUrlRepository>();
            ShortenUrlRepostory.Setup(p => p.GetShortenUrl(It.IsAny<string>())).Returns(Task.FromResult<ShortenUrl>(shortenUrl));
            var shortenUrlService = new ShortenUrlService(ShortenUrlRepostory.Object, new CodeService());

            var result = await shortenUrlService.GetStatsByCode("ABC123");

            var expected = JsonConvert.SerializeObject(expectedStats);
            var resultStats = JsonConvert.SerializeObject(result);

            Assert.Equal(expected, resultStats);
        }


        [Fact]
        public async void GetStatsByCodeNotFound()
        {
            var code = "ABC123";

            var ShortenUrlRepostory = new Mock<IShortenUrlRepository>();
            ShortenUrlRepostory.Setup(p => p.GetShortenUrl(It.IsAny<string>())).Returns(Task.FromResult<ShortenUrl>(null));
            var shortenUrlService = new ShortenUrlService(ShortenUrlRepostory.Object, new CodeService());

            await Assert.ThrowsAsync<NotFoundException>(() => shortenUrlService.GetStatsByCode(code));
        }






    }
}
