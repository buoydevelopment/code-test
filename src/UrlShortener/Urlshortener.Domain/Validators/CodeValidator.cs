using System.Linq;
using UrlShortener.Domain.Interfaces.Validators;

namespace UrlShortener.Domain.Validators
{
    public class CodeValidator : ICodeValidator
    {
        public bool Execute(string code)
        {
            return code.All(x => char.IsLetterOrDigit(x)) && code.Length == 6;
        }
    }
}
