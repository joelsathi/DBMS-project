import { IBaseManager } from "./IBaseManager";

export interface IBaseModel {
  tableName: string;
  manager: IBaseManager
}
