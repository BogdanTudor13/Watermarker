import { Component, OnInit } from '@angular/core';
import { MenuItem } from 'primeng/api';


@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  items: MenuItem[] = [];
  constructor() { }

  ngOnInit(): void {
    this.items = [
      {
        label:'Home',
        icon: 'pi pi-home',
        command: this.showOkay
      },
      {
          label:'File',
          icon:'pi pi-fw pi-file',
          items:[
              {
                  label:'New',
                  icon:'pi pi-fw pi-plus',
                  items:[
                  {
                      label:'Bookmark',
                      icon:'pi pi-fw pi-bookmark'
                  },
                  {
                      label:'Video',
                      icon:'pi pi-fw pi-video'
                  },

                  ]
              },
              {
                  label:'Delete',
                  icon:'pi pi-fw pi-trash'
              },
              {
                  separator:true
              },
              {
                  label:'Export',
                  icon:'pi pi-fw pi-external-link'
              }
          ]
      },
      {
          label:'Edit',
          icon:'pi pi-fw pi-pencil',
          items:[
              {
                  label:'Left',
                  icon:'pi pi-fw pi-align-left'
              },
              {
                  label:'Right',
                  icon:'pi pi-fw pi-align-right'
              },
              {
                  label:'Center',
                  icon:'pi pi-fw pi-align-center'
              },
              {
                  label:'Justify',
                  icon:'pi pi-fw pi-align-justify'
              },

          ]
      },
     
  ];
  }

  showOkay(){
    alert('okay!');
  }

}
