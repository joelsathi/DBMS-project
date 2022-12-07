import { Request, Response } from "express";

export interface ICRUDController {
  create: (req: Request, res: Response) => void;
  getList: (req: Request, res: Response) => void;
  getOne: (req: Request, res: Response) => void;
  delete: (req: Request, res: Response) => void;
  update: (req: Request, res: Response) => void;
}
