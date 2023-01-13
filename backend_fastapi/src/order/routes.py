from fastapi import APIRouter, Response, Request, status
from .models import (
    OrderCartModel,
    ProductOrderModel,
    OrderPaymentDetailModel,
    DeliveryModel,
    LocationModel,
)

from ..auth.utils import checkAdmin

from ..core.pagination import get_pagination, get_params

order_router = APIRouter(
    prefix="/order",
)


@order_router.get("/order_cart")
def get_order_cart_list(
    response: Response,
    request: Request,
):
    checkAdmin(request=request)

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = OrderCartModel.objects.select(
        page_num=page_num,
        page_size=page_size,
        sort_keys=sort_dict,
        filters=where_params,
        get_row_count=True,
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    serialized_rows = [OrderCartModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/order_cart",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@order_router.post("/order_cart")
async def post_order_cart_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = OrderCartModel(**field_dict)
    new_obj.save()


@order_router.get("/product_order")
def get_product_order_list(
    response: Response,
    request: Request,
):
    checkAdmin(request=request)

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = ProductOrderModel.objects.select(
        page_num=page_num,
        page_size=page_size,
        sort_keys=sort_dict,
        filters=where_params,
        get_row_count=True,
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    serialized_rows = [ProductOrderModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/product_order",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@order_router.post("/product_order")
async def post_product_order_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = ProductOrderModel(**field_dict)
    new_obj.save()


@order_router.get("/order_payment_detail")
def get_order_payment_detail_list(
    response: Response,
    request: Request,
):
    checkAdmin(request=request)

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = OrderPaymentDetailModel.objects.select(
        page_num=page_num,
        page_size=page_size,
        sort_keys=sort_dict,
        filters=where_params,
        get_row_count=True,
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    serialized_rows = [OrderPaymentDetailModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/order_payment_detail",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@order_router.post("/order_payment_detail")
async def post_order_payment_detail_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = OrderPaymentDetailModel(**field_dict)
    new_obj.save()


@order_router.get("/delivery")
def get_delivery_list(
    response: Response,
    request: Request,
):
    checkAdmin(request=request)

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = DeliveryModel.objects.select(
        page_num=page_num,
        page_size=page_size,
        sort_keys=sort_dict,
        filters=where_params,
        get_row_count=True,
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    serialized_rows = [DeliveryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/delivery",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@order_router.post("/delivery")
async def post_delivery_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = DeliveryModel(**field_dict)
    new_obj.save()


@order_router.get("/location")
def get_location_list(
    response: Response,
    request: Request,
):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = LocationModel.objects.select(
        page_num=page_num,
        page_size=page_size,
        sort_keys=sort_dict,
        filters=where_params,
        get_row_count=True,
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    serialized_rows = [LocationModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/location",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@order_router.post("/location")
async def post_location_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = LocationModel(**field_dict)
    new_obj.save()
