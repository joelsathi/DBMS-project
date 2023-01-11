from fastapi import APIRouter, Response
from .models import (
    OrderCartModel,
    ProductOrderModel,
    OrderPaymentDetailModel,
    DeliveryModel,
    LocationModel,
)

from ..core.pagination import get_pagination

order_router = APIRouter(
    prefix="/order",
)


@order_router.get("/order_cart")
def get_order_cart_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = OrderCartModel.objects.select_by_page(page_num=page_num, page_size=page_size)
    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [OrderCartModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/order_cart",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@order_router.get("/product_order")
def get_product_order_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = ProductOrderModel.objects.select_by_page(
        page_num=page_num, page_size=page_size
    )
    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [ProductOrderModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/product_order",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@order_router.get("/order_payment_detail")
def get_order_payment_detail_list(
    response: Response, page_num: int = 1, page_size: int = 10
):
    rows = OrderPaymentDetailModel.objects.select_by_page(
        page_num=page_num, page_size=page_size
    )
    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [OrderPaymentDetailModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/order_payment_detail",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@order_router.get("/delivery")
def get_delivery_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = DeliveryModel.objects.select_by_page(page_num=page_num, page_size=page_size)
    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [DeliveryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/delivery",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@order_router.get("/location")
def get_location_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = LocationModel.objects.select_by_page(page_num=page_num, page_size=page_size)
    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [LocationModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/location",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret
