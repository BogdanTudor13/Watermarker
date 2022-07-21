using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Watermarker.Common;
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

        public string ExecuteScript(string args, AlgorithmsEnum algorithm)
        {
            var scriptDotPy = GetScript(algorithm);
            var startInfo = new ProcessStartInfo
            {
                UseShellExecute = false,
                RedirectStandardOutput = true,
                FileName = pythonModel.PythonExe,
                Arguments = $"{scriptDotPy} {args}"
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

        public string GetScript(AlgorithmsEnum algorithm)
        {
            return algorithm switch
            {
                AlgorithmsEnum.DCT_DWT => pythonModel.DctDwt,
                _ => string.Empty,
            };
        }

    }


}
