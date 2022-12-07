import * as dotenv from "dotenv";
import { ConnectionOptions } from "mysql2";

dotenv.config({ path: __dirname + "/../.env" });

interface AppConfig {
  HOST: string;
  PORT: number;
  NODE_ENV: string;
  DB_CONFIG: ConnectionOptions;
  DB_NAME: string;
}

const appConfig: AppConfig = {
  HOST: process.env.HOST || "localhost",
  PORT: process.env.PORT ? parseInt(process.env.PORT) : 3001,
  NODE_ENV: process.env.NODE_ENV || "DEV",
  DB_NAME: process.env.DB_NAME as string, // NOTE: This has to be defined
  DB_CONFIG: {
    port: process.env.DB_PORT ? parseInt(process.env.DB_PORT) : 3306,
    host: process.env.DB_HOST || "127.0.0.1",
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    connectionLimit: process.env.DB_CONNECTION_LIMIT
      ? parseInt(process.env.DB_CONNECTION_LIMIT)
      : 2,
  },
};
export default appConfig;
