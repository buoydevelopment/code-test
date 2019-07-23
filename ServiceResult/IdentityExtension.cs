using Microsoft.AspNetCore.Identity;
using System.Collections.Generic;

namespace server.ServiceResult
{
    public static class IdentityExtension
    {
        public static ServiceResultBase ToServiceResult(this IdentityResult identity)
        {
            var result = new ServiceResult();
            AddErrors(result, identity.Errors);
            return result;
        }

        public static ServiceResult<TReturn> ToServiceResult<TReturn>(this IdentityResult identity, TReturn tReturn)
        {
            var result = new ServiceResult<TReturn>(tReturn);
            AddErrors(result, identity.Errors);
            return result;
        }

        private static void AddErrors(ServiceResultBase result, IEnumerable<IdentityError> errors)
        {
            foreach (var error in errors)
            {
                result.AddNotification(NotificationType.Error, error.Description);
            }
        }
    }
}
