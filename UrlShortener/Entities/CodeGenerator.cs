using System;
using System.Linq;
using UrlShortener.Models;

namespace UrlShortener.Entities
{
    public class CodeGenerator
    {
        public static string GetShortCode(PostNewUrlRequest request)
        {
            var random = new Random();
            const string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
            return new string(Enumerable.Repeat(chars, 6)
              .Select(s => s[random.Next(s.Length)]).ToArray());
        }
    }
}