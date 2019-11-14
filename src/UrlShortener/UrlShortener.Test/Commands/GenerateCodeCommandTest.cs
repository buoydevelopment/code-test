using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;
using UrlShortener.Domain.Commands;
using Xunit;

namespace UrlShortener.Test.Commands
{
    public class GenerateCodeCommandTest
    {
        [Fact]
        public void ShouldGenerateValidLengthCode()
        {
            var length = 6;
            var command = new GenerateCodeCommand();

            var code = command.Execute(length);

            Assert.Equal(length, code.Length);
        }

        [Fact]
        public void ShouldGenerateInvalidValidLengthCode()
        {
            var length = 6;
            var invalidLength = 8;

            var command = new GenerateCodeCommand();

            var code = command.Execute(invalidLength);

            Assert.NotEqual(length, code.Length);
        }


        [Fact]
        public void ShouldGenerateValidAlphanumericCode()
        {
            var length = 6;     

            var command = new GenerateCodeCommand();

            var code = command.Execute(length);

            Assert.True(code.All(x => char.IsLetterOrDigit(x)));
        }

        [Fact]
        public void ShouldGenerateRandomCodes()
        {
            var length = 6;

            var command = new GenerateCodeCommand();

            var codes = new List<string>
            {
                command.Execute(length),
                command.Execute(length),
                command.Execute(length),
                command.Execute(length),
            };

            Assert.True(codes.Distinct().Count() == codes.Count());
        }
    }
}
