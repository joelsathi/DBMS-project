import express, { Request, Response } from "express";
import appConfig from "./config";
import router from "./routes";
import { initDb } from "./db";

initDb();
const app = express();
app.use(router);
app.listen(appConfig.PORT, appConfig.HOST, () => {
  console.log(`Server running on port ${appConfig.PORT}`);
});
