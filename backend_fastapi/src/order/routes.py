from fastapi import APIRouter, Response
from .models import (
    OrderCartModel,
    ProductOrderModel,
    OrderPaymentDetailModel,
    DeliveryModel,
    LocationModel,
)

order_router = APIRouter(
    prefix="/order",
)


@order_router.get("/order_cart")
def get_order_cart_list(response: Response):
    rows = OrderCartModel.objects.select()
    serialized_rows = [OrderCartModel.serialize(row) for row in rows]
    return serialized_rows


@order_router.get("/product_order")
def get_product_order_list(response: Response):
    rows = ProductOrderModel.objects.select()
    serialized_rows = [ProductOrderModel.serialize(row) for row in rows]
    return serialized_rows


@order_router.get("/order_payment_detail")
def get_order_payment_detail_list(response: Response):
    rows = OrderPaymentDetailModel.objects.select()
    serialized_rows = [OrderPaymentDetailModel.serialize(row) for row in rows]
    return serialized_rows


@order_router.get("/delivery")
def get_delivery_list(response: Response):
    rows = DeliveryModel.objects.select()
    serialized_rows = [DeliveryModel.serialize(row) for row in rows]
    return serialized_rows


@order_router.get("/location")
def get_location_list(response: Response):
    rows = LocationModel.objects.select()
    serialized_rows = [LocationModel.serialize(row) for row in rows]
    return serialized_rows
