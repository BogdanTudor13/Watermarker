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

}
