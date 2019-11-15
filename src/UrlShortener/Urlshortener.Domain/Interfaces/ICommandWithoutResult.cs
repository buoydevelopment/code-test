using System;
using System.Collections.Generic;
using System.Text;

namespace UrlShortener.Domain.Interfaces
{
    public interface ICommandWithoutResult<TEntity>
    {
        void Execute(TEntity param);
    }
}
