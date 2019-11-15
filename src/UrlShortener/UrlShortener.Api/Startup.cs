using AutoMapper;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using UrlShortener.Api.Bootstrap.Filters;
using UrlShortener.Domain.Commands;
using UrlShortener.Domain.Interfaces;
using UrlShortener.Domain.Interfaces.Commands;
using UrlShortener.Domain.Interfaces.Creators;
using UrlShortener.Domain.Interfaces.Validators;
using UrlShortener.Domain.Services;
using UrlShortener.Domain.Services.Creators;
using UrlShortener.Domain.Validators;
using UrlShortener.Infra.Data;

namespace UrlShortener.Api
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;

            using (var db = new UrlShortenerContext())
            {
                db.Database.EnsureCreated();
            }
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddTransient(typeof(UrlShortenerContext));
            services.AddTransient(typeof(IRepository<>), typeof(Repository<>));
            services.AddTransient<IUrlShortenerService, UrlShortenerService>();
            services.AddTransient<IGenerateCodeCommand, GenerateCodeCommand>();
            services.AddTransient<ICodeValidator, CodeValidator>();
            services.AddTransient<IUrlShortenerCreatorService, UrlShortenerCreatorService>();
            services.AddTransient<IShortenUrlUsageCommand, ShortenUrlUsageCommand>();

            services.AddAutoMapper(typeof(Startup));
            
            services
                .AddControllers(option =>
            {
                option.Filters.Add(new ExceptionFilter());
            })
                .AddJsonOptions(option =>
            {
                option.JsonSerializerOptions.IgnoreNullValues = true;
            });
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseHttpsRedirection();

            app.UseRouting();

            app.UseAuthorization();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}
