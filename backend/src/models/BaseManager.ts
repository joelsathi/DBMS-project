import { Connection } from "mysql2";
import { IBaseManager } from "./types/IBaseManager";
import { IBaseModel } from "./types/IBaseModel";

export class BaseManager implements IBaseManager {
  db;
  modelClass;

  constructor(
    db: Connection,
    modelClass: { new (...args: any[]): IBaseModel }
  ) {
    this.db = db;
    this.modelClass = modelClass;
  }

  async select({ fields }: { fields?: string[] | string }) {
    const sqlQuery = `SELECT ${
      typeof fields === "string"
        ? fields
        : fields?.length == 0
        ? "*"
        : fields?.join(",")
    } FROM ${new this.modelClass().tableName}`;

    return new Promise((resolve, reject) => {
      this.db.query(sqlQuery, (err, result, fields) => {
        if (err) {
          throw err;
        } else {
          resolve(result);
        }
      });
    });
  }
}
