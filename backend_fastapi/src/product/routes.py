from fastapi import APIRouter, Response, Request, status

from .models import (
    ProductModel,
    ProductVariantModel,
    SubCategoryModel,
    SuperCategoryModel,
    DiscountModel,
    OptionsModel,
    InventoryModel,
    ProductSubCategoryModel,
    ProductVarientOptionsModel,
)

from ..auth.utils import checkAdmin

from ..core.pagination import get_pagination, get_params

product_router = APIRouter(
    prefix="/product",
)


@product_router.get("/product")
def get_product_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = ProductModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [ProductModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/product",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret

@product_router.post("/product")
async def post_product_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = ProductModel(**field_dict)
    new_obj.save()

@product_router.get("/variant")
def get_variant_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = ProductVariantModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [ProductVariantModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/variant",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret

@product_router.post("/variant")
async def post_varient_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = ProductVariantModel(**field_dict)
    new_obj.save()


@product_router.get("/subcategory")
def get_subcategory_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = SubCategoryModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [SubCategoryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/subcategory",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret

@product_router.post("/subcategory")
async def post_subcategory_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = SubCategoryModel(**field_dict)
    new_obj.save()


@product_router.get("/supercategory")
def get_supercategory_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = SuperCategoryModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [SuperCategoryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/supercategory",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret

@product_router.post("/supercategory")
async def post_supercategory_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = SuperCategoryModel(**field_dict)
    new_obj.save()


@product_router.get("/discount")
def get_discount_list(response: Response, request: Request):

    checkAdmin(request=request)

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = DiscountModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [DiscountModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/discount",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret

@product_router.post("/discount")
async def post_discount_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = DiscountModel(**field_dict)
    new_obj.save()


@product_router.get("/options")
def get_options_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = OptionsModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [OptionsModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/options",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret

@product_router.post("/options")
async def post_options_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = OptionsModel(**field_dict)
    new_obj.save()


@product_router.get("/inventory")
def get_inventory_list(response: Response, request: Request):

    checkAdmin(request=request)

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = InventoryModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [InventoryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/inventory",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret

@product_router.post("/inventory")
async def post_inventory_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = InventoryModel(**field_dict)
    new_obj.save()


@product_router.get("/product_subcategory")
def get_product_subcategory_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = ProductSubCategoryModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [ProductSubCategoryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/product_subcategory",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret

@product_router.post("/product_subcategory")
async def post_product_subcategory_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = ProductSubCategoryModel(**field_dict)
    new_obj.save()


@product_router.get("/product_variant_options")
def get_product_variant_options_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = ProductVarientOptionsModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [ProductVarientOptionsModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/product_variant_options",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret

@product_router.post("/product_variant_option")
async def post_product_product_variant_option_list(request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = ProductVarientOptionsModel(**field_dict)
    new_obj.save()

