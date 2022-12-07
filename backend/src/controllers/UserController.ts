import { Request, Response } from "express";
import UserModel from "../models/UserModel";
import { ICRUDController } from "./types/ICRUDController";

class UserController implements ICRUDController {
  create(req: Request, res: Response) {
    throw new Error("Not Implemented");
    // TODO
  }

  getList(req: Request, res: Response) {
    UserModel.manager
      .select({ fields: "*" })
      .then((result) => {
        res.status(200);
        res.json(result);
      })
      .catch((err) => {
        console.log(err);
        res.status(500);
        res.json({ error: "Internal Server Error" });
      });
  }

  getOne(req: Request, res: Response) {
    throw new Error("Not Implemented");
    // TODO
  }

  update(req: Request, res: Response) {
    throw new Error("Not Implemented");
    // TODO
  }

  delete(req: Request, res: Response) {
    throw new Error("Not Implemented");
    // TODO
  }
}

export default new UserController();
