export class Configuration{
    // public content: string | ArrayBuffer | null;
    // public watermark:string | ArrayBuffer | null;
    public content:File;
    public watermark:File;
    public algorithm:number;
    public isEncode:boolean;

    public isAlgorithmSelected:boolean = false;
    public isEncodeSelected:boolean = false;
    public isContentUpload:boolean = false;
    public isWatermarkUpload:boolean = false;

    public key1:number = 0;
    public key2: number|null;
    public key3: number|null;
    public key4: number|null;

    constructor(){
        this.algorithm = 0;
        this.isEncode = true;
    }
}