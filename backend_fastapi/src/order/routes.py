from fastapi import APIRouter, Response\

from .models import OrderCartModel, ProductOrderModel, OrderPaymentDetailModel, DeliveryModel, LocationModel

order_router = APIRouter(
    prefix="/order",
)

@order_router.get("/orderCart")
def get_user_list(response: Response):
    rows = OrderCartModel.objects.select()
    serialized_rows = [OrderCartModel.serialize(row) for row in rows]
    return serialized_rows

@order_router.get("/productOrder")
def get_user_list(response: Response):
    rows = ProductOrderModel.objects.select()
    serialized_rows = [ProductOrderModel.serialize(row) for row in rows]
    return serialized_rows

@order_router.get("/orderPaymentDetail")
def get_user_list(response: Response):
    rows = OrderPaymentDetailModel.objects.select()
    serialized_rows = [OrderPaymentDetailModel.serialize(row) for row in rows]
    return serialized_rows

@order_router.get("/delivery")
def get_user_list(response: Response):
    rows = DeliveryModel.objects.select()
    serialized_rows = [DeliveryModel.serialize(row) for row in rows]
    return serialized_rows

@order_router.get("/location")
def get_user_list(response: Response):
    rows = LocationModel.objects.select()
    serialized_rows = [LocationModel.serialize(row) for row in rows]
    return serialized_rows