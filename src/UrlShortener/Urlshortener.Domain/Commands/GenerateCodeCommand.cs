using UrlShortener.CrossCutting;
using UrlShortener.Domain.Interfaces.Commands;

namespace UrlShortener.Domain.Commands
{
    public class GenerateCodeCommand : IGenerateCodeCommand
    {
        public string Execute(int lenght)
        {
            return CodeUtilities.Generate(lenght);
        }
    }
}
