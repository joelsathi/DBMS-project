import express, { Request, Response } from "express";

const router = express.Router();
router.get("/", (req: Request, res: Response) => {
  res.send("Hello World");
});
router.get("/about", (req: Request, res: Response) => {
  res.json({ projectName: "Thulasi", description: "Some Description" });
});

const app = express();
app.use(router);
const host = "localhost";
const port = 3001;
app.listen(port, host, () => {
  console.log(`Server running on port ${port}`);
});
