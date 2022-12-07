import { IBaseModel } from "./types/IBaseModel";
import { db } from "../db";
import { IBaseManager } from "./types/IBaseManager";
import { BaseManager } from "./BaseManager";

interface IUser {
  id: number;
  isRegistered: boolean;
  registered_user_id: number | null;
}

// TODO this needs a lot more functionality
class UserModel implements IBaseModel {
  tableName = "user";
  manager: BaseManager;

  constructor() {
    this.manager = new BaseManager(db, UserModel);
  }
}

export default new UserModel();
