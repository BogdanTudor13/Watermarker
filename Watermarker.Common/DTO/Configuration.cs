using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Watermarker.Common.DTO
{
    public class Configuration
    {
        public string Content { get; set; }

        public string Watermark { get; set; }

        public int Algorithm { get; set; }

        public bool IsEncode { get; set; }

        public byte[] ArrayContent { get; set; }
        public byte[] WatermarkContent { get; set; }

    }
}
