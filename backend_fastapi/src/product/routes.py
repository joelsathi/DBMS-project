from fastapi import APIRouter, Response

from .models import ProductModel, ProductVariantModel, SubCategoryModel, SuperCategoryModel, DiscountModel, OptionsModel, InventoryModel, ProductSubCategoryModel, ProductVarientOptionsModel

product_router = APIRouter(
    prefix="/product",
)

@product_router.get("/product")
def get_user_list(response: Response):
    rows = ProductModel.objects.select()
    serialized_rows = [ProductModel.serialize(row) for row in rows]
    return serialized_rows

@product_router.get("/variant")
def get_user_list(response: Response):
    rows = ProductVariantModel.objects.select()
    serialized_rows = [ProductVariantModel.serialize(row) for row in rows]
    return serialized_rows

@product_router.get("/subCategory")
def get_user_list(response: Response):
    rows = SubCategoryModel.objects.select()
    serialized_rows = [SubCategoryModel.serialize(row) for row in rows]
    return serialized_rows

@product_router.get("/superCategory")
def get_user_list(response: Response):
    rows = SuperCategoryModel.objects.select()
    serialized_rows = [SuperCategoryModel.serialize(row) for row in rows]
    return serialized_rows

@product_router.get("/discount")
def get_user_list(response: Response):
    rows = DiscountModel.objects.select()
    serialized_rows = [DiscountModel.serialize(row) for row in rows]
    return serialized_rows

@product_router.get("/options")
def get_user_list(response: Response):
    rows = OptionsModel.objects.select()
    serialized_rows = [OptionsModel.serialize(row) for row in rows]
    return serialized_rows

@product_router.get("/inventory")
def get_user_list(response: Response):
    rows = InventoryModel.objects.select()
    serialized_rows = [InventoryModel.serialize(row) for row in rows]
    return serialized_rows

@product_router.get("/productSubCategory")
def get_user_list(response: Response):
    rows = ProductSubCategoryModel.objects.select()
    serialized_rows = [ProductSubCategoryModel.serialize(row) for row in rows]
    return serialized_rows

@product_router.get("/productVarientOptions")
def get_user_list(response: Response):
    rows = ProductVarientOptionsModel.objects.select()
    serialized_rows = [ProductVarientOptionsModel.serialize(row) for row in rows]
    return serialized_rows
