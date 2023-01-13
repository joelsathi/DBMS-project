from fastapi import APIRouter, Request, status, Response

from ..core.db import connection_pool

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

    rows, total_rows = ProductModel.objects.select(
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

    serialized_rows = [ProductModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/product",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    # set the cache-control header on the response(since home page once loaded is static)
    # browser to cache the response for 3600 seconds, or 1 hour.
    response.headers["Cache-Control"] = "max-age=3600"
    return ret


@product_router.post("/product")
async def post_product(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = ProductModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@product_router.put("/product/{id}")
async def put_product(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["sku"] = id
    upd_obj = ProductModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@product_router.delete("/product/{id}")
def delete_product(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = ProductModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


@product_router.get("/product/{id}")
def get_product_by_id(id: int, response: Response):
    row = ProductModel.objects.select_by_id(id)
    if row is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        # TODO create a error response class
        return {
            "Error": "Detail Not Found",
            "Message": "Product with id {} not found".format(id),
        }

    return ProductModel.serialize_with_related(row)


@product_router.get("/product_filtered/search")
def get_filtered_product_list(
    category: str,
    subCategory: str,
    query: str,
    response: Response,
    request: Request,
    page_num: int = 1,
    page_size: int = 10,
):

    # TODO add field validation

    if category or subCategory or query:
        sql_query_where = " WHERE "
        checks = []
        if category:
            checks.append("super_category.cat_name = '{}'".format(category))
        if subCategory:
            checks.append("sub_category.name = '{}'".format(subCategory))
        if query:
            checks.append("p.name LIKE '%{}%'".format(query))
        sql_query_where += " AND ".join(checks)
        start = (page_num - 1) * page_size
        # TODO discount_id didn't work p.discount_id,
        # TODO way to get column names in product
        sql_query_str = "SELECT p.id, p.name, p.description, p.base_price, p.brand, p.image_url FROM product p \
                JOIN product_sub_category ON p.id = product_sub_category.product_id \
                JOIN sub_category ON product_sub_category.subcategory_id = sub_category.id \
                JOIN super_category ON sub_category.super_category_id =  super_category.id\
                {} LIMIT {} OFFSET {}".format(
            sql_query_where,
            page_size,
            start,
        )

        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute(sql_query_str)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        total_rows = 4  # NEED TO IMPLEMENT THE FUNCTION
        # serialized_rows = [SubCategoryModel.serialize(row) for row in rows]
        serialized_rows = []
        for row in rows:
            serialized_row = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "base_price": row[3],
                "brand": row[4],
                "image_url": row[5],
            }
            serialized_rows.append(serialized_row)
    else:
        page_num, page_size, sort_dict, where_params = get_params(request.query_params)

        # TODO add field validation

        rows, total_rows = ProductModel.objects.select(
            page_num=page_num,
            page_size=page_size,
            sort_keys=sort_dict,
            filters=where_params,
            get_row_count=True,
        )
        serialized_rows = [ProductModel.serialize(row) for row in rows]
    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    ret = get_pagination(
        "/product",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.get("/variant")
def get_variant_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = ProductVariantModel.objects.select(
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

    serialized_rows = [ProductVariantModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/variant",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.post("/variant")
async def post_variant(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = ProductVariantModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@product_router.put("/variant/{id}")
async def put_variant(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = ProductVariantModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@product_router.delete("/variant/{id}")
def delete_variant(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = ProductVariantModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


@product_router.get("/product_variant_filtered/search")
def get_filtered_variant(
    id: int, sku: str, response: Response, page_num: int = 1, page_size: int = 10
):
    # TODO add field validation
    if sku or id:
        start = (page_num - 1) * page_size
        sql_query_str = ""
        rows = None
        if sku:
            # TODO way to get column names, foriegn key product_variant.product_id,
            sql_query_str = "SELECT product_variant.sku, product_variant.name,  product_variant.price, product_variant.image_url, product.brand FROM product_variant \
                    JOIN product ON product_variant.product_id = product.id \
                    WHERE product_variant.sku = '{}' LIMIT {} OFFSET {}".format(
                sku,
                page_size,
                start,
            )
            cnx = connection_pool.get_connection()
            cursor = cnx.cursor()
            cursor.execute(sql_query_str)
            rows = cursor.fetchall()
            cursor.close()
            cnx.close()

            total = 4  # NEED TO IMPLEMENT THE FUNCTION
            # serialized_rows = [SubCategoryModel.serialize(row) for row in rows]
            serialized_rows = []
            for row in rows:
                serialized_row = {
                    "sku": row[0],
                    "name": row[1],
                    "price": row[2],
                    "image_url": row[3],
                    "brand": row[4],
                }
                serialized_rows.append(serialized_row)
        else:
            sql_query_str = "SELECT p.id, p.name, p.description, p.base_price, p.brand, p.image_url FROM product p \
                    WHERE p.id = '{}' LIMIT {} OFFSET {}".format(
                id,
                page_size,
                start,
            )

            cnx = connection_pool.get_connection()
            cursor = cnx.cursor()
            cursor.execute(sql_query_str)
            rows = cursor.fetchall()
            cursor.close()
            cnx.close()

            total = 4  # NEED TO IMPLEMENT THE FUNCTION
            # serialized_rows = [SubCategoryModel.serialize(row) for row in rows]
            serialized_rows = []
            for row in rows:
                serialized_row = {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "base_price": row[3],
                    "brand": row[4],
                    "image_url": row[5],
                }
                serialized_rows.append(serialized_row)
        if rows is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "Error": "Detail not Found",
                "Message": "No entries on page {}".format(page_num),
            }
        # ret = get_pagination(
        #     "/product",
        #     total=total,
        #     serialized_rows=serialized_rows,
        #     page_num=page_num,
        #     page_size=page_size,
        # )

        return serialized_rows


@product_router.get("/variants/{id}")
def get_filtered_variants(
    id: int,
    response: Response,
    request: Request,
    page_num: int = 1,
    page_size: int = 10,
):
    # TODO add field validation
    if id:
        sql_query_where = " WHERE "
        checks = []
        if id:
            checks.append("product_variant.product_id = '{}'".format(id))
        sql_query_where += " AND ".join(checks)
        start = (page_num - 1) * page_size
        # TODO way to get column names, foriegn key product_variant.product_id,
        sql_query_str = "SELECT product_variant.sku, product_variant.name,  product_variant.price, product_variant.image_url FROM product_variant \
                {} LIMIT {} OFFSET {}".format(
            sql_query_where,
            page_size,
            start,
        )
        cnx = connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute(sql_query_str)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        total_rows = 4  # NEED TO IMPLEMENT THE FUNCTION
        # serialized_rows = [SubCategoryModel.serialize(row) for row in rows]
        serialized_rows = []
        for row in rows:
            serialized_row = {
                "sku": row[0],
                "name": row[1],
                "price": row[2],
                "image_url": row[3],
            }
            serialized_rows.append(serialized_row)
    else:

        page_num, page_size, sort_dict, where_params = get_params(request.query_params)

        # TODO add field validation

        rows, total_rows = ProductVariantModel.objects.select(
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

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }
    ret = get_pagination(
        "/variant",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.get("/subcategory")
def get_subcategory_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = SubCategoryModel.objects.select(
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

    serialized_rows = [SubCategoryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/subcategory",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.post("/subcategory")
async def post_subcategory(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = SubCategoryModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@product_router.put("/subcategory/{id}")
async def put_subcategory(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = SubCategoryModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@product_router.delete("/subcategory/{id}")
def delete_subcategory(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = SubCategoryModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


@product_router.get("/subcategory_filtered/search")
def get_filtered_subcategories(
    category: str,
    response: Response,
    request: Request,
    page_num: int = 1,
    page_size: int = 10,
):

    # TODO add field validation
    sql_query_where = ""
    if category:
        sql_query_where = " WHERE super_category.cat_name = '{}'".format(category)
    start = (page_num - 1) * page_size
    # TODO way to get column names in subcategory
    sql_query_str = "SELECT sub_category.id, sub_category.name, sub_category.description FROM sub_category \
            JOIN super_category ON sub_category.super_category_id =  super_category.id\
            {} LIMIT {} OFFSET {}".format(
        sql_query_where,
        page_size,
        start,
    )

    cnx = connection_pool.get_connection()
    cursor = cnx.cursor()
    cursor.execute(sql_query_str)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = 4  # NEED TO IMPLEMENT THE FUNCTION
    # serialized_rows = [SubCategoryModel.serialize(row) for row in rows]
    serialized_rows = []
    for row in rows:
        serialized_row = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
        }
        serialized_rows.append(serialized_row)

    ret = get_pagination(
        "/subcategory",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )

    return ret


@product_router.get("/supercategory")
def get_supercategory_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = SuperCategoryModel.objects.select(
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

    serialized_rows = [SuperCategoryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/supercategory",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.post("/supercategory")
async def post_supercategory(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = SuperCategoryModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@product_router.put("/supercategory/{id}")
async def put_supercategory(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = SuperCategoryModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@product_router.delete("/supercategory/{id}")
def delete_supercategory(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = SuperCategoryModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


@product_router.get("/discount")
def get_discount_list(response: Response, request: Request):

    checkAdmin(request=request)

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = DiscountModel.objects.select(
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

    serialized_rows = [DiscountModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/discount",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.post("/discount")
async def post_discount(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = DiscountModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@product_router.put("/discount/{id}")
async def put_discount(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = DiscountModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@product_router.delete("/discount/{id}")
def delete_discount(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = DiscountModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


@product_router.get("/options")
def get_options_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = OptionsModel.objects.select(
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

    serialized_rows = [OptionsModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/options",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.post("/options")
async def post_options(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = OptionsModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@product_router.put("/options/{id}")
async def put_options(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = OptionsModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@product_router.delete("/options/{id}")
def delete_options(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = OptionsModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


@product_router.get("/options/{id}")
def get_filtered_options(
    id: int,
    response: Response,
    request: Request,
    page_num: int = 1,
    page_size: int = 10,
):

    # TODO add field validation
    sql_query_where = ""
    if id:
        sql_query_where = " WHERE p.id = '{}'".format(id)
    start = (page_num - 1) * page_size
    # TODO way to get column names in subcategory
    sql_query_str = "SELECT options.option_id, options.prod_description, options.price_diff FROM options \
            JOIN product_variant_option pvo ON options.option_id=pvo.option_id \
            JOIN product_variant pv ON pv.sku=pvo.sku\
            JOIN product p ON pv.product_id=p.id\
            {} LIMIT {} OFFSET {}".format(
        sql_query_where,
        page_size,
        start,
    )

    cnx = connection_pool.get_connection()
    cursor = cnx.cursor()
    cursor.execute(sql_query_str)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = 4  # NEED TO IMPLEMENT THE FUNCTION
    # serialized_rows = [SubCategoryModel.serialize(row) for row in rows]
    serialized_rows = []
    for row in rows:
        serialized_row = {
            "option_id": row[0],
            "prod_description": row[1],
            "price_diff": row[2],
        }
        serialized_rows.append(serialized_row)

    ret = get_pagination(
        "/product",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )

    return ret


@product_router.get("/inventory")
def get_inventory_list(response: Response, request: Request):

    checkAdmin(request=request)

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = InventoryModel.objects.select(
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

    serialized_rows = [InventoryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/inventory",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.post("/inventory")
async def post_inventory(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = InventoryModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@product_router.put("/inventory/{id}")
async def put_inventory(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = InventoryModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@product_router.delete("/inventory/{id}")
def delete_inventory(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = InventoryModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


@product_router.get("/product_subcategory")
def get_product_subcategory_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = ProductSubCategoryModel.objects.select(
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

    serialized_rows = [ProductSubCategoryModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/product_subcategory",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.post("/product_subcategory")
async def post_product_subcategory(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = ProductSubCategoryModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@product_router.put("/product_subcategory/{id}")
async def put_product_subcategory(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = ProductSubCategoryModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@product_router.delete("/product_subcategory/{id}")
def delete_product_subcategory(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = ProductSubCategoryModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


@product_router.get("/product_variant_options")
def get_product_variant_options_list(response: Response, request: Request):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = ProductVarientOptionsModel.objects.select(
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

    serialized_rows = [ProductVarientOptionsModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/product_variant_options",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@product_router.post("/product_variant_option")
async def post_product_variant_option(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = ProductVarientOptionsModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@product_router.put("/product_variant_option/{id}")
async def put_product_variant_option(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = ProductVarientOptionsModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@product_router.delete("/product_variant_option/{id}")
def delete_product_variant_option(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = ProductVarientOptionsModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}
