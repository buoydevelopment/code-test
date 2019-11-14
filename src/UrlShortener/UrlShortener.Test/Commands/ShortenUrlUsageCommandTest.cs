using System;
using System.Collections.Generic;
using System.Text;
using UrlShortener.Domain.Commands;
using UrlShortener.Domain.Entities;
using Xunit;

namespace UrlShortener.Test.Commands
{
    public class ShortenUrlUsageCommandTest
    {
        [Fact]
        public void ShouldUpdateCountAndLastUsage()
        {
            var entity = new ShortUrl
            { 
                LastUsage = null,
                UsageCount = 0
            };

            var command = new ShortenUrlUsageCommand();

            var code = command.Execute(entity);
            
            Assert.Equal(1, entity.UsageCount);
            Assert.NotNull(entity.LastUsage);
        }

        [Fact]
        public void ShouldUpdateCountAndLastUsageNow()
        {
            var origDate = DateTime.Now;

            var entity = new ShortUrl
            {
                LastUsage = origDate,
                UsageCount = 1
            };

            var command = new ShortenUrlUsageCommand();

            var code = command.Execute(entity);

            Assert.Equal(2, entity.UsageCount);
            Assert.True(entity.LastUsage > origDate);
        }
    }
}
