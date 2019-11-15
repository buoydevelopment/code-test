using AutoMapper;
using System.Linq;
using System.Threading.Tasks;
using UrlShortener.CrossCutting.Exceptions;
using UrlShortener.Domain.Entities;
using UrlShortener.Domain.Interfaces;
using UrlShortener.Domain.Interfaces.Validators;
using UrlShortener.Domain.Services.UrlShortenerCreatorService;

namespace UrlShortener.Domain.Services.Creators
{
    public class UrlShortenerCreatorService : UrlShortenerBaseCreatorService
    {
        private readonly IRepository<ShortUrl> repository;
        private readonly ICodeValidator codeValidator;

        public UrlShortenerCreatorService(IMapper mapper,
            IRepository<ShortUrl> repository,
            ICodeValidator codeValidator) : base(mapper)
        {
            this.repository = repository;
            this.codeValidator = codeValidator;
        }

        protected override void ConflictEntity(string code)
        {
            throw new ConflictException($"Code [{code}] is already in use");
        }

        protected override  bool IsConflictEntity(string code)
        {
           var task = Task.Run(async () => await this.repository.ListAsync(x => x.Code.Equals(code)));

            var result = task.Result;

            return result.FirstOrDefault() != null;
        }

        protected override bool IsValid(string code)
        {
            return this.codeValidator.Execute(code);
        }

        protected override void UnprocessableEntity()
        {
            throw new UnprocessableEntityException($"Code must be Alphanumeric and 6 chars lenght");
        }
    }
}
