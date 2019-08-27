using System;
using System.Collections.Generic;
using System.Text;

namespace shortenurl.model.Interfaces.Services
{
    public interface ICodeService
    {
        bool IsCodeValid(string Code);
        string GenerateCode(int length, Random random);
    }
}
