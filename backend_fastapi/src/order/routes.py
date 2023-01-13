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
async def post_order_cart(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = OrderCartModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@order_router.put("/order_cart/{id}")
async def put_order_cart(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = OrderCartModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@order_router.delete("/order_cart/{id}")
def delete_order_cart(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = OrderCartModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


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
async def post_product_order(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = ProductOrderModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@order_router.put("/product_order/{id}")
async def put_product_order(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = ProductOrderModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@order_router.delete("/product_order/{id}")
def delete_product_order(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = ProductOrderModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


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
async def post_order_payment_detail(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = OrderPaymentDetailModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@order_router.put("/order_payment_detail/{id}")
async def put_order_payment_detail(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = OrderPaymentDetailModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@order_router.delete("/order_payment_detail/{id}")
def delete_order_payment_detail(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = OrderPaymentDetailModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


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
async def post_delivery(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = DeliveryModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@order_router.put("/delivery/{id}")
async def put_delivery(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = DeliveryModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@order_router.delete("/delivery/{id}")
def delete_delivery(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = DeliveryModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


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
async def post_location(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = LocationModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@order_router.put("/location/{id}")
async def put_location(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = LocationModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@order_router.delete("/location/{id}")
def delete_location(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = LocationModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}