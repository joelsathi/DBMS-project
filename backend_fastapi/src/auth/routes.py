from fastapi import APIRouter, Response

from .models import UserDBModel

user_router = APIRouter(
    prefix="/auth",
)


@user_router.get("/user")
def get_user_list(response: Response):
    rows = UserDBModel.manager.select()
    return rows
