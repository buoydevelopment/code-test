using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Service.Common;
using Test.Dto;
using Test.Service.Interfaces;
using Shortener.Core.Extensions;
using Shortener.Core;
using Test.Data;
using System.Linq;
using Test.Data.Entities;
using Microsoft.EntityFrameworkCore;


namespace Test.Service.Services
{
    public class UrlService : IUrlService
    {
        private readonly TestContext DB;
       
        public UrlService()
        {
            DB = new TestContext();
           
        }
       

        public async Task<UrlDto> GetUrl(string Code)
        {
            return await (from x in DB.Urls.Where(x => x.Code == Code)
                          select new UrlDto { Code = x.Code, SourceUrl = x.SourceUrl, Usage_Count=x.Usage_Count, Last_Usage = x.Last_Usage }).SingleOrDefaultAsync();
        }

        public async Task<ServiceResult<string>> CreateShortCode(SourceUrlDto entity)
        {
            var result = new ServiceResult<string>();

            try
            {
                Boolean isValid = true;
               try
                {
                    entity.Url.ValidateUrl();
                }
                catch(Exception)
                {
                    result.AddError("", "Invalid Url");
                    isValid = false;
                }
              
                if(isValid)
                {
                    var codeResult = await this.GenerateShortCode(entity);
                    result.Response = codeResult.Code.ToString();
                }

                return result;

            }
            catch (Exception e)
            {
                result.AddError("", e.InnerException.ToString());
            }

            return result;
        }

        private async Task<Url> GenerateShortCode(SourceUrlDto sourceUrl)
        {
            
            var existing = await this.IsAlreadyShortened(sourceUrl.Url);
            if (existing != null)
            {
                existing.Usage_Count = existing.Usage_Count + 1;
                existing.Last_Usage = DateTime.Now;
                await DB.SaveChangesAsync();

                return existing;
            }
            else
            {
                var code = await this.GetCode(sourceUrl);

                var shortCode = new Url { Id = Guid.NewGuid().ToString(), SourceUrl = sourceUrl.Url, Start_Date = DateTime.UtcNow, Code = code };

                DB.Urls.Add(shortCode);
                await DB.SaveChangesAsync();

                return shortCode;
            }
            
        }
        protected async Task<string> GetCode(SourceUrlDto sourceUrl)
        {
            var code ="";
            var existing = await DB.Urls.SingleOrDefaultAsync(x=>x.SourceUrl== sourceUrl.Url);
            if (existing == null)
            {
                if(sourceUrl.Code=="")
                {
                    code = ShortCodeGenerator.Generate();
                }
                else
                {
                    code = sourceUrl.Code;
                 }
             
            }
            else
            {
                code = existing.Code;
            }
            return code;
        }

        protected  async Task<Data.Entities.Url> IsAlreadyShortened(string url)
        {
            string baseLink = url.UrlToBase64();
            var link = await DB.Urls.Where(x => x.SourceUrl == url).SingleOrDefaultAsync();
            if (link == null)
            {
                return null;
            }

            return  link;
        }


    }

    
}
