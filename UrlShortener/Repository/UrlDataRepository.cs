using Newtonsoft.Json;
using System;
using System.IO;
using UrlShortener.Contracts;
using UrlShortener.Entities;
using UrlShortener.Models;

namespace UrlShortener.Repository
{
    public class UrlDataRepository : IUrlDataRepository
    {
        private string dbPath;

        private UrlDataList CreateConnection()
        {
            UrlDataList db = null;
            dbPath = AppDomain.CurrentDomain.BaseDirectory + "db.json";
            if (!File.Exists(dbPath))
                File.Create(dbPath);
            using (FileStream s = File.Open(dbPath, FileMode.Open))
            using (StreamReader sr = new StreamReader(s))
            using (JsonReader reader = new JsonTextReader(sr))
            {
                while (reader.Read())
                {
                    db = new JsonSerializer().Deserialize<UrlDataList>(reader);
                }
            }

            if (db == null)
                db = new UrlDataList();

            return db;
        }

        public bool PostNewUrl(PostNewUrlRequest request, string code)
        {
            var db = CreateConnection();

            var urlData = db.UrlList.Find(x => x.Code == code);
            if (urlData != null)
                return false;

            urlData = new UrlData()
            {
                Code = code,
                URL = request.Url,
                Start_Date = DateTime.Now,
                Usage_Count = 0
            };
            db.UrlList.Add(urlData);

            using (StreamWriter sw = new StreamWriter(dbPath))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                new JsonSerializer().Serialize(writer, db);
            }
            return true;
        }

        public Uri GetUrl(string code)
        {
            var db = CreateConnection();

            var urlData = db.UrlList.Find(x => x.Code == code);
            if (urlData == null)
                return null;

            urlData.Usage_Count++;
            urlData.Last_Usage = DateTime.Now;
            using (StreamWriter sw = new StreamWriter(dbPath))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                new JsonSerializer().Serialize(writer, db);
            }

            return new Uri(urlData.URL);
        }

        public GetUrlStatsResponse GetUrlStats(string code)
        {
            var db = CreateConnection();

            var urlData = db.UrlList.Find(x => x.Code == code);
            if (urlData == null)
                return null;

            return new GetUrlStatsResponse()
            {
                Created_at = urlData.Start_Date,
                Usage_count = urlData.Usage_Count,
                Last_usage = urlData.Last_Usage
            };
        }
    }
}