using Microsoft.AspNetCore.Mvc;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using System.Net;
using UrlShortener.Models;

namespace UrlShortener.Tests.Controllers
{
    [TestClass]
    public class PostNewUrlTests : MainControllerTests
    {
        [TestMethod]
        public void PostNewUrlTests_Success()
        {
            urlDataRepository.Setup(x => x.PostNewUrl(It.IsAny<PostNewUrlRequest>(), It.IsAny<string>())).Returns(true);

            var request = new PostNewUrlRequest()
            {
                Code = "Test12",
                Url = "http://www.google.com"
            };
            var response = urlsController.PostNewUrl(request);
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is CreatedResult);
            Assert.IsTrue(((CreatedResult)response).Value is PostNewUrlResponse);
        }

        [TestMethod]
        public void PostNewUrlTests_EmptyCode_Success()
        {
            urlDataRepository.Setup(x => x.PostNewUrl(It.IsAny<PostNewUrlRequest>(), It.IsAny<string>())).Returns(true);

            var request = new PostNewUrlRequest()
            {
                Code = "",
                Url = "http://www.google.com"
            };
            var response = urlsController.PostNewUrl(request);
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is CreatedResult);
            Assert.IsTrue(((CreatedResult)response).Value is PostNewUrlResponse);
        }

        [TestMethod]
        public void PostNewUrlTests_EmptyUrl_Error()
        {
            var request = new PostNewUrlRequest()
            {
                Code = "Test12",
                Url = ""
            };
            var response = urlsController.PostNewUrl(request);
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is BadRequestResult);
        }

        [TestMethod]
        public void PostNewUrlTests_CodeConflict_Error()
        {
            urlDataRepository.Setup(x => x.PostNewUrl(It.IsAny<PostNewUrlRequest>(), It.IsAny<string>())).Returns(false);

            var request = new PostNewUrlRequest()
            {
                Code = "Test12",
                Url = "http://www.google.com"
            };
            var response = urlsController.PostNewUrl(request);
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is ConflictResult);
        }

        [TestMethod]
        public void PostNewUrlTests_UnprocessableCode_Error()
        {
            var request = new PostNewUrlRequest()
            {
                Code = "Test1234",
                Url = "http://www.google.com"
            };
            var response = urlsController.PostNewUrl(request);
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is UnprocessableEntityResult);

            request.Code = "Te%&12";
            response = urlsController.PostNewUrl(request);
            Assert.IsTrue(response is IActionResult);
            Assert.IsTrue(response is UnprocessableEntityResult);
        }
    }
}
