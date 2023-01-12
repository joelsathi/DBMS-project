from fastapi import APIRouter, Response

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

from ..core.pagination import get_pagination

product_router = APIRouter(
    prefix="/product",
)


@product_router.get("/product")
def get_product_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = ProductModel.objects.select_by_page(page_num=page_num, page_size=page_size)
    total = 2  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [ProductModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/product",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.get("/variant")
def get_variant_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = ProductVariantModel.objects.select_by_page(
        page_num=page_num, page_size=page_size
    )
    total = 2  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [ProductVariantModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/variant",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.get("/subcategory")
def get_subcategory_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = SubCategoryModel.objects.select_by_page(
        page_num=page_num, page_size=page_size
    )
    total = 2  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [SubCategoryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/subcategory",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.get("/supercategory")
def get_supercategory_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = SuperCategoryModel.objects.select_by_page(
        page_num=page_num, page_size=page_size
    )
    total = 2  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [SuperCategoryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/supercategory",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.get("/discount")
def get_discount_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = DiscountModel.objects.select_by_page(page_num=page_num, page_size=page_size)
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


@product_router.get("/options")
def get_options_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = OptionsModel.objects.select_by_page(page_num=page_num, page_size=page_size)
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


@product_router.get("/inventory")
def get_inventory_list(response: Response, page_num: int = 1, page_size: int = 10):
    rows = InventoryModel.objects.select_by_page(page_num=page_num, page_size=page_size)
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


@product_router.get("/product_subcategory")
def get_product_subcategory_list(
    response: Response, page_num: int = 1, page_size: int = 10
):
    rows = ProductSubCategoryModel.objects.select_by_page(
        page_num=page_num, page_size=page_size
    )
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


@product_router.get("/product_variant_options")
def get_product_variant_options_list(
    response: Response, page_num: int = 1, page_size: int = 10
):
    rows = ProductVarientOptionsModel.objects.select_by_page(
        page_num=page_num, page_size=page_size
    )
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
