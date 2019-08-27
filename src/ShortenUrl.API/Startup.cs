using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Newtonsoft.Json;
using shortenurl.api.Filters;
using shortenurl.model;
using shortenurl.model.Interfaces;
using shortenurl.model.Interfaces.Repositories;
using shortenurl.model.Interfaces.Services;
using shortenurl.model.Repositories;
using shortenurl.model.Services;
using shortenurl.model.Settings;

namespace shortenurl.api
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc(
                    options =>
                    options.Filters.Add(new CustomExceptionFilter())
                )
                .SetCompatibilityVersion(CompatibilityVersion.Version_2_1)
                    .AddJsonOptions(options =>
               {
                   //Set date configurations
                   options.SerializerSettings.DateTimeZoneHandling = DateTimeZoneHandling.Utc;
                   options.SerializerSettings.ReferenceLoopHandling = ReferenceLoopHandling.Ignore;
               });


            var connectionStringsSection = Configuration.GetSection("ConnectionStrings");
            services.Configure<ConnectionStrings>(connectionStringsSection);

            services.AddSingleton<IShortenUrlService, ShortenUrlService>();
            services.AddSingleton<ISqlDataAccess, SqlDataAccess>();
            services.AddSingleton<IShortenUrlRepository, ShortenUrlRepository>();
            services.AddSingleton<ICodeService, CodeService>();
            
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseHsts();
            }

            app.UseHttpsRedirection();
            app.UseMvc();
        }
    }
}
