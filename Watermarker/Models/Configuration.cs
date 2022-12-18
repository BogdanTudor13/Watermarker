using Microsoft.AspNetCore.Http;
using System.Text.Json.Serialization;

namespace Watermarker.Models
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
