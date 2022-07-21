import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DecodeComponent } from './components/decode/decode.component';
import { EncodeComponent } from './components/encode/encode.component';
import { HomeComponent } from './components/home/home.component';

const routes: Routes = [
  {path: 'encode', component:EncodeComponent},
  {path: 'decode', component:DecodeComponent},
  {path: 'home',component:HomeComponent },
  {path:'',redirectTo:'home',pathMatch:'full'},
  {path: '**', redirectTo: ''}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
