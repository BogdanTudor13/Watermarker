using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using Watermarker.Common;
using Watermarker.Common.DTO;
using Watermarker.Common.Enums;

namespace Watermarker.Services
{
    public class PythonService
    {
        private PythonModel pythonModel;
        public PythonService(PythonModel pythonModel)
        {
            this.pythonModel = pythonModel;
        }

        public string ExecuteScript(Configuration configuration)
        {
            ConvertString2ByteArray(configuration);

            var scriptDotPy = GetScript(configuration);

            var startInfo = new ProcessStartInfo
            {
                UseShellExecute = false,
                RedirectStandardOutput = true,
                FileName = pythonModel.PythonExe,
                Arguments = $"{scriptDotPy}"
            };

            using (var process = Process.Start(startInfo))
            {
                using (var reader = process.StandardOutput)
                {
                    var result = reader.ReadToEnd();
                    return result;
                }
            }
        }

        public string GetScript(Configuration configuration)
        {
            StringBuilder pythonScript = new(pythonModel.ScriptsLocation);

            pythonScript.Append(((AlgorithmsEnum)configuration.Algorithm).ToString());
            
            pythonScript.Append(configuration.IsEncode ? "_encode" : "_decode");
            pythonScript.Append(".py");

            return pythonScript.ToString();
        }

        private void ConvertString2ByteArray(Configuration model)
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
        }

        public bool SaveImagesOnDisk(Configuration model)
        {
            return true;
        }

    }


}
