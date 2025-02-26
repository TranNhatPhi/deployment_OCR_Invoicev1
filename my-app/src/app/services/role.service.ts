import {Injectable} from "@angular/core";
import {environment} from "../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn:'root'
})
export class RoleService {
  private apiGetRoles = `${environment.apiBaseurl}/roles`;
  constructor(private http:HttpClient){}
  getRoles():Observable<any>{
    return this.http.get<any[]>(this.apiGetRoles);
  }
}
