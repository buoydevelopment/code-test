using System;
using System.Collections.Generic;
using System.Text;

namespace UrlShortener.Domain.Interfaces
{
    public interface ICommandWithResult<TEntity, TResult>
    {
        TResult Execute(TEntity param);
    }
}
