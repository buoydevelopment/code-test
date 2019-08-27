using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace shortenurl.model.Interfaces
{
    public interface ISqlDataAccess
    {
        Task Execute(string procedureName, Dictionary<string, object> listParams);
        Task<T> GetOne<T>(string procedureName, Dictionary<string, object> listParams);
    }
}
