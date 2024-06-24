using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
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
        public async Task<IActionResult> Post([FromForm] WatermarkRequest request)
        {
            var originalImagePath = Path.Combine(Path.GetTempPath(), request.OriginalImage.FileName);
            var watermarkImagePath = Path.Combine(Path.GetTempPath(), request.WatermarkImage.FileName);

            using (var stream = new FileStream(originalImagePath, FileMode.Create))
            {
                await request.OriginalImage.CopyToAsync(stream);
            }

            using (var stream = new FileStream(watermarkImagePath, FileMode.Create))
            {
                await request.WatermarkImage.CopyToAsync(stream);
            }

            var fileName = pythonModel.ScriptsLocation + "main.py";
            var processStartInfo = new ProcessStartInfo
            {
                FileName = pythonModel.PythonExe,
                Arguments = $"{fileName} {originalImagePath} {watermarkImagePath} {request.Key1} {request.Key2} {request.Key3} {request.Key4} {request.AlgorithmKey}",
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            var process = Process.Start(processStartInfo);
            var output = process.StandardOutput.BaseStream;

            return File(output, "image/png");
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
