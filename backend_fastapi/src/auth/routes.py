from fastapi import APIRouter, Response, status

from .models import RegisteredUserDBModel, UserDBModel, PaymentDetailDBModel

user_router = APIRouter(
    prefix="/auth",
)


@user_router.get("/registered_user")
def get_registered_user_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = RegisteredUserDBModel.objects.select_by_page(page_num=page_num, page_size=page_size)
    total = 18
    serialized_rows = [RegisteredUserDBModel.serialize(row) for row in rows]
    
    start = (page_num - 1) * page_size
    end = start + page_size

    ret = {
        "data": serialized_rows,
        "total": total,
        "count": page_size,
        "pagination": {}
    }

    if end >= total:
        ret["pagination"]["next"] = None

        if page_num > 1:
            ret["pagination"]["previous"] = f"/registered_user?page_num={page_num-1}&page_size={page_size}"
        else:
            ret["pagination"]["previous"] = None
    else:
        if page_num > 1:
            ret["pagination"]["previous"] = f"/registered_user?page_num={page_num-1}&page_size={page_size}"
        else:
            ret["pagination"]["previous"] = None

        ret["pagination"]["next"] = f"/registered_user?page_num={page_num+1}&page_size={page_size}"

    return ret
    # return serialized_rows


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
