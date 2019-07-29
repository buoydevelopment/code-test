using System;
using System.Collections.Generic;
using System.Text;
using Microsoft.EntityFrameworkCore;
using Test.Data.Entities;

namespace Test.Data
{
    public class TestContext : DbContext
    {
        public TestContext()
        {
        }
        public TestContext(DbContextOptions<TestContext> ConnectionStrings)
         : base(ConnectionStrings)
        {
        }
        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);
            {
            }
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseSqlServer(ConnectionString);

        }

        public static string ConnectionString { get; set; }
        public virtual DbSet<Url> Urls { get; set; }
    }
}
