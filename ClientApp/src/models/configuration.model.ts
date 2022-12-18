export class Configuration{
    public content: string | ArrayBuffer | null;
    public watermark:string | ArrayBuffer | null;
    public algorithm:number;
    public isEncode:boolean;

    public isAlgorithmSelected:boolean = false;
    public isEncodeSelected:boolean = false;
    public isContentUpload:boolean = false;
    public isWatermarkUpload:boolean = false;

    constructor(){
        this.algorithm = 1;
        this.isEncode = true;
    }
}