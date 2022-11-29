import express, { Request, Response } from "express";
import appConfig from "./config";
import mysql2, { Connection } from "mysql2";

const db: Connection = mysql2.createConnection(appConfig.DB_CONFIG);
db.connect((err: any) => {
  if (err) {
    throw err
  } else {
    console.log("Connected to mysql database")
  }
})

const router = express.Router();
router.get("/", (req: Request, res: Response) => {
  res.send("Hello World");
});
router.get("/about", (req: Request, res: Response) => {
  res.json({ projectName: "Thulasi", description: "Some Description" });
});

const app = express();
app.use(router);
app.listen(appConfig.PORT, appConfig.HOST, () => {
  console.log(`Server running on port ${appConfig.PORT}`);
});
