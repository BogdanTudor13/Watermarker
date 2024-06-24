using Microsoft.AspNetCore.Http;

namespace Watermarker.Common.DTO
{
    public class WatermarkRequest
    {
        public IFormFile OriginalImage { get; set; }
        public IFormFile WatermarkImage { get; set; }
        public int Key1 { get; set; }
        public int? Key2 { get; set; }
        public int? Key3 { get; set; }
        public int? Key4 { get; set; }
        public bool IsEncode { get; set; }
        public int AlgorithmKey { get; set; }
    }
}
