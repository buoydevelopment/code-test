using shortenurl.model.Interfaces.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace shortenurl.model.Services
{
    public class CodeService : ICodeService
    {
        public string GenerateCode(int length, Random random)
        {
            string allowedCharacters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
            StringBuilder result = new StringBuilder(length);
            for (int i = 0; i < length; i++)
            {
                result.Append(allowedCharacters[random.Next(allowedCharacters.Length)]);
            }
            return result.ToString();
        }

        public bool IsCodeValid(string code)
        {
            return (code.All(char.IsLetterOrDigit) && code.Length == 6);
        }
    }
}
