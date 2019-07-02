using Microsoft.AspNetCore.Mvc;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using System;
using System.Net;
using System.Net.Http;

namespace UrlShortener.Tests.Controllers
{
    [TestClass]
    public class GetUrlTests : MainControllerTests
    {
        [TestMethod]
        public void GetUrlTests_Success()
        {
            urlDataRepository.Setup(x => x.GetUrl(It.IsAny<string>())).Returns(new Uri("http://www.google.com/"));

            var response = urlsController.GetUrl("Test12");
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is RedirectResult);
            Assert.IsTrue(((RedirectResult)response).Url.Equals("http://www.google.com/"));
        }

        [TestMethod]
        public void GetUrlTests_Code_NotFound_Error()
        {
            urlDataRepository.Setup(x => x.GetUrl("Test12")).Returns(new Uri("http://www.google.com/"));

            var response = urlsController.GetUrl("12Test");
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is NotFoundResult);
        }

        [TestMethod]
        public void GetUrlTests_EmptyCode_NotFound_Error()
        {
            var response = urlsController.GetUrl(String.Empty);
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is NotFoundResult);
        }
    }
}
