import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Configuration } from 'src/models/configuration.model';
import { ValidatorModel } from 'src/models/validator.model';
import {ApiServiceService} from './services/api-service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent implements OnInit {

  @ViewChild("encodeDropdown") encodeDropdown : ElementRef;
  @ViewChild("algorithmDropdown") algorithmDropdown : ElementRef;

  configuration:Configuration = new Configuration();
  key1: number;
  key2: number;
  key3: number;
  key4: number;
  ngOnInit(): void {
  }

  constructor(private apiService: ApiServiceService){}

  selectEncodeDropdown(option:number):void{
    if(option == 1){
      this.encodeDropdown.nativeElement.innerText = 'Inserează watermark'
      this.configuration.isEncode = true;
      this.configuration.isEncodeSelected = true;
    }
    if(option == 2){
      this.encodeDropdown.nativeElement.innerText = 'Extrage watermark'
      this.configuration.isEncode = false;
      this.configuration.isEncodeSelected = true;
    }
  }

  selectAlgorithmDropdown(option: number):void{
    if(option == 1){
      this.algorithmDropdown.nativeElement.innerText = 'DCT + JPEG Quantization table'
      this.configuration.isAlgorithmSelected = true;
    }
    if(option == 2){
      this.algorithmDropdown.nativeElement.innerText = 'DWT + DCT'
      this.configuration.isAlgorithmSelected = true;
    }
    if(option == 3){
      this.algorithmDropdown.nativeElement.innerText = 'Algoritm propriu dezvoltat'
      this.configuration.isAlgorithmSelected = true;
    }
    this.configuration.algorithm = option;
  }

  onImageSelected(event:any){
    this.configuration.content = event.target.files[0];
    console.log(this.configuration);
    this.configuration.isContentUpload = true;

    this.configuration.content = event.target.files[0];
    // var file = event.target.files[0];
    // var fileReader = new FileReader();
    // fileReader.readAsArrayBuffer(file);
    // fileReader.onload = () =>{
    //   if(fileReader.result && fileReader.result instanceof ArrayBuffer){
    //     this.configuration.content = new Uint8Array(fileReader.result);
    //   }
    // }
  }

  onWatermarkSelected(event:any){
    this.configuration.watermark = event.target.files[0];
    console.log(this.configuration);
    this.configuration.isWatermarkUpload = true;
    this.configuration.watermark = event.target.files[0];
    // var file = event.target.files[0];
    // var fileReader = new FileReader();
    // fileReader.readAsArrayBuffer(file);
    // fileReader.onload = () =>{
    //   if(fileReader.result && fileReader.result instanceof ArrayBuffer){
    //     this.configuration.watermark = new Uint8Array(fileReader.result);
    //   }
    // }
  }

  submit(){
    const validator = this.isValidConfiguration();
    if(!validator.isValid){
      return;
    }
    
    this.configuration.key1 = this.key1;
    this.configuration.key2 = this.key2;
    this.configuration.key3 = this.key3;
    this.configuration.key4 = this.key4;

    const formData = new FormData();
    formData.append('originalImage', this.configuration.content);
    formData.append('watermarkImage', this.configuration.watermark);
    formData.append('key1', this.key1.toString());
    formData.append('key2', this.key2?.toString() ?? '');
    formData.append('key3', this.key3?.toString() ?? '');
    formData.append('key4', this.key4?.toString() ?? '');
    formData.append('algorithmKey', this.configuration.algorithm.toString());
    formData.append('isEncode', this.configuration.isEncode?.toString() ?? '');
    this.apiService.exec(formData, this.configuration.isEncode);
    //send to API
  }

  isValidConfiguration():ValidatorModel{
    if(!this.configuration.isEncodeSelected){
      return new ValidatorModel(false, "Alegeți tipul de acțiune!");
    }
    if(!this.configuration.isAlgorithmSelected){
      return new ValidatorModel(false, "Alegeți algoritmul de codare!");
    }
    if(!this.configuration.isContentUpload){
      return new ValidatorModel(false, "Selectați imaginea");
    }
    if(this.configuration.isEncode && !this.configuration.isWatermarkUpload)
    {
      return new ValidatorModel(false, "Selectați watermark");
    }
    return new ValidatorModel(true);
  }

  
  title = 'Watermarker';
}
