using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace Test.Data.Entities
{
    public class EntityBase
    {
        [StringLength(128)]
        public string Id { get; set; }

        [System.ComponentModel.DefaultValue(typeof(DateTime), "")]
        public DateTime? Start_Date { get; set; }

        [System.ComponentModel.DefaultValue(typeof(DateTime), "")]
        public DateTime? Last_Usage { get; set; }

        [DefaultValue(0)]
        public bool? IsDeleted { get; set; }

        //[NotMapped]
        //public string Name { get; set; }
        public EntityBase()
        {
            this.Start_Date = DateTime.Now;
            this.Last_Usage = DateTime.Now;
            this.IsDeleted = false;
            this.Id = Guid.NewGuid().ToString();
        }
    }
}
