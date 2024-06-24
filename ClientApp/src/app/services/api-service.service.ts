import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Configuration } from 'src/models/configuration.model';


const URL = "https://localhost:44314/Main/"

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {

  constructor(private http:HttpClient) {
   }

  ping(configuration:Configuration){
    return this.http.post(URL+"ping",configuration);
  }
  exec(form:FormData, isEncode:boolean){
    return this.http.post(URL + "exec", form, {responseType:'blob'}).subscribe(response=>{
      const blob = new Blob([response], { type: 'image/png' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        let name = 'result.png';
        if(isEncode){
          name = 'watermark_image.png';
        }
        else{
          name = 'extracted_watermark';
        }
        a.download = name;
        a.click();
        window.URL.revokeObjectURL(url);
    });
  }

}
