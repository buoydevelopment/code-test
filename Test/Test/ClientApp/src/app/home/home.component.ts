import { Component, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
})
export class HomeComponent {

  public urls: Url;
  formGroup: FormGroup;
  myBaseUrl: string;
  myHttp: HttpClient;
  public codeResult: string;
  myError: string;

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
    },
      (err: any) => { err => this.myError = err.error.errorMessages; });
  }
  

  getUrl() {

    var code = this.formGroup.controls["code"].value;

    this.myHttp.get<any>(this.myBaseUrl + 'api/Url/GetUrlByCode/Code=' + code).subscribe(result => {
      this.urls = result;
    }, error => console.error(error));
  }

}

interface Url {
  sourceUrl: string;
  targetUrl: string;
  last_Usage: Date;
  cCode: string;
  usage_Count: number;
}

