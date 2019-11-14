using Microsoft.EntityFrameworkCore;
using System.Reflection;
using UrlShortener.Domain.Entities;

namespace UrlShortener.Infra.Data
{
    public class UrlShortenerContext : DbContext
    {
        public DbSet<ShortUrl> ShortUrls { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseSqlite("Filename=UrlShortener.db", options =>
            {
                options.MigrationsAssembly(Assembly.GetExecutingAssembly().FullName);
            });

            base.OnConfiguring(optionsBuilder);
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<ShortUrl>().ToTable("URLShortener", "url");
            modelBuilder.Entity<ShortUrl>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => e.Code).IsUnique();
                entity.Property(e => e.CreatedAt).HasDefaultValueSql("CURRENT_TIMESTAMP");
            });

            base.OnModelCreating(modelBuilder);
        }
    }
}
