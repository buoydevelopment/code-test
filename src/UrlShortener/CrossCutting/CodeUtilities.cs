using System;
using System.Linq;

namespace UrlShortener.CrossCutting
{
    public static class CodeUtilities
    {
        private static string source = "abcdefghijklmnopqrstuvwxyz0123456789";
        private static readonly Random random;

        static CodeUtilities()
        {
            random = new Random();
        }

        public static string Generate(int lengh) => CreateRandomWord(lengh);

        private static string CreateRandomWord(int length)
        {
            return new string(Enumerable.Range(1, length)
                                        .Select(_ => source[new Random().Next(source.Length)])
                                        .ToArray());
        }
    }
}
