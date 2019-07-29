import { Component, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
})
export class HomeComponent {

  public url: Url;
  formGroup: FormGroup;
  myBaseUrl: string;
  myHttp: HttpClient;
  public codeResult: string="";
  myError: string="";

  constructor(http: HttpClient,
    @Inject('BASE_URL') baseUrl: string,
    public fb: FormBuilder,
    public router: Router,
    public avRoute: ActivatedRoute) {

    this.myBaseUrl = baseUrl;
    this.myHttp = http;

    this.createForm();
  }

  createForm() {
    this.formGroup = this.fb.group({
      code: [''],
      url: ['', Validators.required]
    });
  }

  onSubmit() {

    this.myHttp.post<any>(this.myBaseUrl + 'api/Url/Create', this.formGroup.value).subscribe(result => {
      this.codeResult = result;
      this.myError = "";
    },
      (err: any) => {
        this.myError = err.error.errorMessages;
      });
  }
  

  getUrl() {

    var code = this.formGroup.controls["code"].value;

    this.myHttp.get<ResponseUrl>(this.myBaseUrl + 'api/Url/GetUrlByCode?Code=' + code).subscribe(result => {
    
      window.open(result.location, '_self');
    },
      (err: any) => {
        this.myError = err.error.title;
      });
  }


  getUrlInfo() {

    var code = this.formGroup.controls["code"].value;

    this.myHttp.get<Url>(this.myBaseUrl + 'api/Url/GetInfoUrlByCode/' + code + '/stats').subscribe(result => {
      this.url = result;
      
    },
      (err: any) => {
        this.myError = err.error.title;
      });
  }
}





interface Url {
  sourceUrl: string;
  targetUrl: string;
  last_Usage: Date;
  created: Date;
  code: string;
  usage_Count: number;
}

interface ResponseUrl {
  location: string;
}
