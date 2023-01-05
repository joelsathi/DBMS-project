from fastapi import APIRouter, Response, status

from .models import RegisteredUserDBModel, UserDBModel, PaymentDetailDBModel

user_router = APIRouter(
    prefix="/auth",
)


@user_router.get("/registered_user")
def get_registered_user_list(response: Response):
    rows = RegisteredUserDBModel.objects.select()
    serialized_rows = [RegisteredUserDBModel.serialize(row) for row in rows]
    return serialized_rows


@user_router.get("/registered_user/{id}")
def get_registered_user(id: int, response: Response):
    row = RegisteredUserDBModel.objects.select_by_id(id)
    if row is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        # TODO create a error response class
        return {
            "Error": "Detail Not Found",
            "Message": "RegisteredUser with id {} not found".format(id),
        }

    return RegisteredUserDBModel.serialize_with_related(row)


@user_router.get("/user")
def get_user_list(response: Response):
    rows = UserDBModel.objects.select()
    serialized_rows = [UserDBModel.serialize(row) for row in rows]
    return serialized_rows


@user_router.get("/payment_detail")
def get_payment_detail_list(response: Response):
    rows = PaymentDetailDBModel.objects.select()
    serialized_rows = [PaymentDetailDBModel.serialize(row) for row in rows]
    return serialized_rows
