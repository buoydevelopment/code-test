using Microsoft.Extensions.Options;
using shortenurl.model.Interfaces;
using shortenurl.model.Settings;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace shortenurl.model
{
    public class SqlDataAccess : ISqlDataAccess
    {
        private readonly ConnectionStrings _connString;
        public SqlDataAccess(IOptions<ConnectionStrings> connStrings)
        {
            _connString = connStrings.Value;
            var conn = _connString.DefaultConnection;
            if (string.IsNullOrEmpty(conn))
                throw new Exception("The connection string is empty. " +
                     "Please add an entry in the settings.json file with the key 'DefaultConnection' containing the connection string. " +
                     "Or set the connection string on 'connectionKey' parameter");

            
            
        }
     
        private async Task<SqlConnection> NewConnection()
        {
            var conn = new SqlConnection(_connString.DefaultConnection);
            await conn.OpenAsync();
            return conn;
        }


        private void SetParams(SqlCommand cmd, Dictionary<string, object> listParams)
        {
            foreach (var param in listParams)
            {
                cmd.Parameters.Add(new SqlParameter(param.Key, param.Value));

            }
        }

        private T DataReaderMapToObject<T>(IDataReader dr)
        {
            T obj = default(T);

            var columNames = new List<string>();

            for (int i = 0; i < dr.FieldCount; i++)
            {
                columNames.Add(dr.GetName(i));
            }

            if (dr.Read())
            {
                obj = Activator.CreateInstance<T>();
                foreach (PropertyInfo prop in obj.GetType().GetProperties())
                {

                    if (columNames.Contains(prop.Name) && !object.Equals(dr[prop.Name], DBNull.Value))
                    {
                        prop.SetValue(obj, dr[prop.Name], null);
                    }

                }
            }
            return obj;
        }


        public async Task Execute(string procedureName, Dictionary<string, object> listParams)
        {
            using (var conn = await NewConnection())
            {
                using (var cmd = new SqlCommand(procedureName, conn))
                {

                    cmd.CommandType = CommandType.StoredProcedure;
                    cmd.CommandTimeout = 0;
                    SetParams(cmd, listParams);
                    await cmd.ExecuteNonQueryAsync();

                }
            }
        }


        public async  Task<T> GetOne<T>(string procedureName, Dictionary<string, object> listParams)
        {
            T mappedObj;

            using (var conn = await NewConnection())
            {
                using (var cmd = new SqlCommand(procedureName, conn))
                {
                    cmd.CommandType = CommandType.StoredProcedure;

                    SetParams(cmd, listParams);


                    var reader = cmd.ExecuteReader();

                    mappedObj = DataReaderMapToObject<T>(reader);
                }

            }
            return mappedObj;
        }


    }
}
