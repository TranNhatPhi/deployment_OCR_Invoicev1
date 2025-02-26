import {IsNotEmpty, IsString} from "class-validator";

export class CrawlsDataDto {
  @IsString()
  @IsNotEmpty()
  url:string;
  cateId:number;

  constructor(data: any) {
    this.url = data.url;
    this.cateId=data.cateId;
  }
}
