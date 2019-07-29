using Service.Common;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using Test.Data.Entities;
using Test.Dto;

namespace Test.Service.Interfaces
{
    public interface IUrlService: IServiceBase
    {
        
        Task<LocationDto> GetUrl(string Code);
        Task<UrlDto> GetInfoUrl(string Code);
        Task<ServiceResult<string>> CreateShortCode(SourceUrlDto model);
      
    }
}
