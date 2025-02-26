import {Injectable} from "@angular/core";
import {environment} from "../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({

  providedIn: 'root',
})
export class CrawlsDataService {
  private apiUrl = `${environment.apiBaseurl}/crawldata/generateFakeProducts1`;

constructor(private http: HttpClient) {}
  apiCrawlData(body:any): Observable<any>{
      return this.http.post(this.apiUrl,body);
  }
}
