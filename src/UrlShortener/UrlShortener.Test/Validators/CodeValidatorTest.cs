using System;
using System.Collections.Generic;
using System.Text;
using UrlShortener.Domain.Commands;
using UrlShortener.Domain.Validators;
using Xunit;

namespace UrlShortener.Test.Validators
{
    public class CodeValidatorTest
    {
        [Fact]
        public void ShouldGenerateValidLengthCode()
        {
            var length = 6;
            var command = new GenerateCodeCommand();

            var code = command.Execute(length);

            var validator = new CodeValidator();

            Assert.True(validator.Execute(code));
        }

        [Fact]
        public void ShouldGenerateInvalidLengthCode()
        {
            var length = 8;
            var command = new GenerateCodeCommand();

            var code = command.Execute(length);

            var validator = new CodeValidator();

            Assert.False(validator.Execute(code));
        }

        [Fact]
        public void ShouldBeValidCode()
        {
            var code = "aaa123";

            var validator = new CodeValidator();

            Assert.True(validator.Execute(code));
        }

        [Fact]
        public void ShouldBeInvalidCode()
        {
            var code = "aaabbb1";

            var validator = new CodeValidator();

            Assert.False(validator.Execute(code));
        }
    }
}
