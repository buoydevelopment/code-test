using Microsoft.AspNetCore.Mvc;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using System;
using UrlShortener.Models;

namespace UrlShortener.Tests.Controllers
{
    [TestClass]
    public class GetUrlStatsTests : MainControllerTests
    {
        [TestMethod]
        public void GetUrlStatsTests_Success()
        {
            urlDataRepository.Setup(x => x.GetUrlStats(It.IsAny<string>())).Returns(new GetUrlStatsResponse()
            {
                Created_at = DateTime.Now,
                Last_usage = DateTime.Now,
                Usage_count = 1
            });

            var response = urlsController.GetUrlStats("Test12");
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is OkObjectResult);
            Assert.IsTrue(((OkObjectResult)response).Value is GetUrlStatsResponse);
        }

        [TestMethod]
        public void GetUrlStatsTests_Code_NotFound_Error()
        {
            urlDataRepository.Setup(x => x.GetUrlStats("Test12")).Returns(new GetUrlStatsResponse()
            {
                Created_at = DateTime.Now,
                Last_usage = DateTime.Now,
                Usage_count = 1
            });

            var response = urlsController.GetUrlStats("12Test");
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is NotFoundResult);
        }

        [TestMethod]
        public void GetUrlStatsTests_EmptyCode_NotFound_Error()
        {
            var response = urlsController.GetUrlStats(String.Empty);
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is NotFoundResult);
        }
    }
}
