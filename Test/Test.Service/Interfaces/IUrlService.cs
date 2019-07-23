using Service.Common;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using Test.Dto;

namespace Test.Service.Interfaces
{
    public interface IUrlService: IServiceBase
    {
      
        Task<ServiceResult<UrlDto>> GetUrl(string Url);
        Task<ServiceResult<string>> CreateShortCode(SourceUrlDto model);
       
    }
}
