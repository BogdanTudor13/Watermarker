using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Watermarker.Common;
using Watermarker.Common.Enums;
using Watermarker.Services;

namespace Watermarker.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class MainController : ControllerBase
    {
        private readonly IConfiguration configuration;
        private PythonService pythonService;

        private PythonModel pythonModel;
        public MainController(IConfiguration configuration)
        {
            this.configuration = configuration;
            pythonModel = new PythonModel()
            {
                PythonExe = configuration.GetSection("PythonLocation").Value,
                DctDwt = configuration.GetSection("DctDwlLocation").Value
            };
            pythonService = new PythonService(pythonModel);
        }

        [HttpGet("exec")]
        public IActionResult ExecuteScript()
        {
            var result = pythonService.ExecuteScript(string.Empty, AlgorithmsEnum.DCT_DWT);
            return Ok(result);
        }
    }
}
