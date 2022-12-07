import { Connection } from "mysql2";
import { IBaseModel } from "./IBaseModel";

export interface IBaseManager {
  db: Connection;
  modelClass: { new(...args: any[]): IBaseModel }; // TODO there should be a better way to do this

  // methods
  select: ({ fields }: { fields?: string[] | string }) => Promise<any>;
  // TODO update: () => Promise<any>
}
