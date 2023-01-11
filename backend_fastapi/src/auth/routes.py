from fastapi import APIRouter, Response, status, Request

from .models import RegisteredUserDBModel, UserDBModel, PaymentDetailDBModel

from ..core.pagination import get_pagination, get_params

user_router = APIRouter(
    prefix="/auth",
)


@user_router.get("/registered_user")
# "{BASE_URL}/auth/registered_user?page_num=1&page_size=10&sort_by=id,username&sort_order=ASC,DESC&username=thulasithang"
def get_registered_user_list(
    response: Response,
    request: Request,
):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = RegisteredUserDBModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = 18  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [RegisteredUserDBModel.serialize(row) for row in rows]

    ret = get_pagination(
        "/registered_user",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )

    return ret


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
def get_user_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = UserDBModel.objects.select_by_page(page_num=page_num, page_size=page_size)
    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [UserDBModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/user",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@user_router.get("/payment_detail")
def get_payment_detail_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = PaymentDetailDBModel.objects.select_by_page(
        page_num=page_num, page_size=page_size
    )
    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [PaymentDetailDBModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/payment_detail",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret
