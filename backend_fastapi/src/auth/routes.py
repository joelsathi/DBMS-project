from fastapi import APIRouter, Response

from .models import RegisteredUserDBModel, UserDBModel, PaymentDetailDBModel

user_router = APIRouter(
    prefix="/auth",
)


@user_router.get("/registered_user")
def get_user_list(response: Response):
    rows = RegisteredUserDBModel.objects.select()
    serialized_rows = [RegisteredUserDBModel.serialize(row) for row in rows]
    return serialized_rows

@user_router.get("/user")
def get_user_list(response: Response):
    rows = UserDBModel.objects.select()
    serialized_rows = [UserDBModel.serialize(row) for row in rows]
    return serialized_rows

@user_router.get("/paymentDetail")
def get_user_list(response: Response):
    rows = PaymentDetailDBModel.objects.select()
    serialized_rows = [PaymentDetailDBModel.serialize(row) for row in rows]
    return serialized_rows