using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace shortenurl.model.DTOs
{
    public class ShortenUrlDTO
    {
        [Required]
        [Url]
        public string Url { get; set; }

        public string Code { get; set; }
    }
}
