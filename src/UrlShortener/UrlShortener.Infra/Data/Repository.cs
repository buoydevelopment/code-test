using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;
using UrlShortener.Domain.Entities;
using UrlShortener.Domain.Interfaces;

namespace UrlShortener.Infra.Data
{
    public class Repository<T> : IRepository<T> where T : BaseEntity
    {
        private readonly UrlShortenerContext context;
        private readonly DbSet<T> dbset;

        public Repository(UrlShortenerContext context)
        {
            this.context = context;
            this.dbset = this.context.Set<T>();
        }

        public void Add(T entity)
        {
            this.dbset.Add(entity);

            this.context.SaveChanges();
        }

        public void Delete(T entity)
        {
            dbset.Remove(entity);
        }

        public T GetById(string id)
        {
            return dbset.FirstOrDefault(x => x.Id.Equals(id));
        }

        public async Task<T> GetByIdAsync(string id)
        {
            return await dbset.FirstOrDefaultAsync(x => x.Id.Equals(id));
        }

        public async Task<IList<T>> ListAsync(Expression<Func<T, bool>> filter = null)
        {
            IQueryable<T> query = dbset;

            if (filter != null)
            {
                query = query.Where(filter);
            }

            return await query.ToListAsync();
        }

        public void Update(T entity)
        {
            this.dbset.Update(entity);

            this.context.SaveChanges();
        }
    }
}
