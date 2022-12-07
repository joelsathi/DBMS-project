import appConfig from "./config";
import mysql2, { Connection } from "mysql2";

export const db: Connection = mysql2.createConnection(appConfig.DB_CONFIG);

export const initDb = () => {
  db.connect((err: any) => {
    if (err) {
      throw err;
    } else {
      console.log("Connected to Mysql database");
    }
  });
};
