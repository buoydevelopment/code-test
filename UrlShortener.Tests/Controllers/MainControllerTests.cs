using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using UrlShortener.Contracts;
using UrlShortener.Controllers;

namespace UrlShortener.Tests.Controllers
{
    [TestClass]
    public class MainControllerTests
    {
        protected Mock<IUrlDataRepository> urlDataRepository;
        protected UrlsController urlsController;

        public MainControllerTests()
        {
            urlDataRepository = new Mock<IUrlDataRepository>();
            urlsController = new UrlsController(urlDataRepository.Object);
        }
    }
}
