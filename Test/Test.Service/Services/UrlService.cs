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

namespace Test.Service.Services
{
    public class UrlService : IUrlService
    {
      

        public async Task<ServiceResult<UrlDto>> GetByID(string Url)
        {
            var result = new ServiceResult<UrlDto>();

            try
            {

                UrlDto model = new UrlDto();
                model.TargetUrl = this.MakeTinyUrl(Url);

                result.Response = model;

            }
            catch (Exception e)
            {
                result.AddError("", e.InnerException.ToString());
            }

            return result;
        }

       

        protected string ToTinyURLS(string txt)
        {
            Regex regx = new Regex("http://([\\w+?\\.\\w+])+([a-zA-Z0-9\\~\\!\\@\\#\\$\\%\\^\\&amp;\\*\\(\\)_\\-\\=\\+\\\\\\/\\?\\.\\:\\;\\'\\,]*)?", RegexOptions.IgnoreCase);

            MatchCollection mactches = regx.Matches(txt);

            foreach (Match match in mactches)
            {
                string tURL = MakeTinyUrl(match.Value);
                txt = txt.Replace(match.Value, tURL);
            }

            return txt;
        }

        public  string MakeTinyUrl(string Url)
        {
            try
            {
                if (Url.Length <= 12)
                {
                    return Url;
                }
                if (!Url.ToLower().StartsWith("http") && !Url.ToLower().StartsWith("ftp"))
                {
                    Url = "http://" + Url;
                }
                var request = WebRequest.Create("http://tinyurl.com/api-create.php?url=" + Url);
                var res = request.GetResponse();
                string text;
                using (var reader = new StreamReader(res.GetResponseStream()))
                {
                    text = reader.ReadToEnd();
                }
                return text;
            }
            catch (Exception)
            {
                return Url;
            }
        }

        public async Task<ServiceResult<UrlDto>> GetUrl(string Url)
        {
            var result = new ServiceResult<UrlDto>();

            try
            {

                UrlDto model = new UrlDto();
                model.TargetUrl = Url.ValidateUrl();

                result.Response = model;

            }
            catch (Exception e)
            {
                result.AddError("", e.InnerException.ToString());
            }

            return result;
        }

        public async Task<ServiceResult<string>> CreateShortCode(SourceUrlDto entity)
        {
            var result = new ServiceResult<string>();

            try
            {

                UrlDto model = new UrlDto();
                model.TargetUrl = entity.Url.ValidateUrl();

                result.Response = model.TargetUrl;

            }
            catch (Exception e)
            {
                result.AddError("", e.InnerException.ToString());
            }

            return result;
        }
    }
}
