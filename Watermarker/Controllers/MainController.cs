using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using System.Linq;
using Watermarker.Common;
using Watermarker.Common.DTO;
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
                ScriptsLocation = configuration.GetSection("ScriptsLocation").Value,
                FolderSaveLocation = configuration.GetSection("FolderSaveLocation").Value
            };
            pythonService = new PythonService(pythonModel);
        }

        [HttpPost("exec")]
        public IActionResult ExecuteScript(Configuration model)
        {
            var result = pythonService.ExecuteScript(model);
            return Ok(result);
        }

        [HttpPost("ping")]
        public IActionResult Ping(Configuration model)
        {
            var stringContent = model.Content.Split(",");
            model.ArrayContent = new byte[stringContent.Length];
            for (var index = 0; index < stringContent.Length; index++)
            {
                model.ArrayContent[index] = byte.Parse(stringContent[index]);
            }
            var watermarkContent = model.Watermark.Split(",");
            model.WatermarkContent = new byte[watermarkContent.Length];
            for (var index = 0; index < watermarkContent.Length; index++)
            {
                model.WatermarkContent[index] = byte.Parse(stringContent[index]);
            }
            return Ok(model);
        }
    }
}
