from fastapi import APIRouter, Response

from .models import RegisteredUserDBModel

user_router = APIRouter(
    prefix="/auth",
)


@user_router.get("/registered_user")
def get_user_list(response: Response):
    rows = RegisteredUserDBModel.objects.select()
    serialized_rows = [RegisteredUserDBModel.serialize(row) for row in rows]
    return serialized_rows
