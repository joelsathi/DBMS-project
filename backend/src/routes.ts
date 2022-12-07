import express, { Request, Response } from "express";
import UserController from "./controllers/UserController";

const router = express.Router();
router.get("/", (req: Request, res: Response) => {
  res.send("Hello World");
});
router.get("/about", (req: Request, res: Response) => {
  res.json({ projectName: "Thulasi", description: "Some Description" });
});

// User routes
router.get("/user", UserController.getList)
router.post("/user", UserController.create)
router.get("/user/:id", UserController.getOne)
router.delete("/user/:id", UserController.delete)
router.put("/user/:id", UserController.update)

export default router;
