from fastapi import APIRouter, Request, status, Response

from ..core.db import connection_pool

from ..auth.utils import checkAdmin

from ..core.pagination import get_pagination, get_params

report_router = APIRouter(
    prefix="/reports",
)



@report_router.get("/quarterly_sales_report/search")
def get_quarterly_sales_report(
    year: str,
    response: Response,
    request: Request,
    page_num: int = 1,
    page_size: int = 10,
):

    # TODO add field validation
    if year is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": "Bad Request", "Message": "Missing year"}
    start = (page_num - 1) * page_size
    sql_query_str = "SELECT p.id, p.sku, YEAR(o.billing_date) AS year ,\
        SUM(CASE WHEN MONTH(o.billing_date) IN (1,2,3) THEN p.quantity END) AS firstQuaterQty,\
        SUM(CASE WHEN MONTH(o.billing_date) IN (1,2,3) THEN p.price END) AS firstQuaterSales,\
        SUM(CASE WHEN MONTH(o.billing_date) IN (4,5,6) THEN p.quantity END) AS secondQuaterQty,\
        SUM(CASE WHEN MONTH(o.billing_date) IN (4,5,6) THEN p.price END) AS secondQuaterSales,\
        SUM(CASE WHEN MONTH(o.billing_date) IN (7,8,9) THEN p.quantity END) AS thirdQuaterQty,\
        SUM(CASE WHEN MONTH(o.billing_date) IN (7,8,9) THEN p.price END) AS thirdQuaterSales,\
        SUM(CASE WHEN MONTH(o.billing_date) IN (10,11,12) THEN p.quantity END) AS fourthQuaterQty,\
        SUM(CASE WHEN MONTH(o.billing_date) IN (10,11,12) THEN p.price END) AS fourthQuaterSales,\
        SUM(p.quantity) AS total \
        FROM product_order p \
        JOIN order_cart o on o.order_id = p.order_id\
        WHERE YEAR(o.billing_date) = '{}' \
        GROUP BY YEAR(o.billing_date), p.id\
        ORDER BY firstQuaterSales DESC, secondQuaterSales DESC, thirdQuaterSales DESC, fourthQuaterSales DESC\
        LIMIT {} OFFSET {}".format(
        year,
        page_size,
        start,
    )
    cnx = connection_pool.get_connection()
    cursor = cnx.cursor()
    cursor.execute(sql_query_str)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    total_rows = 10 # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = []
    for row in rows:
        serialized_row = {
            "id": row[0],
            "sku": row[1],
            "year": row[2],
            "firstQuaterQty": row[3],
            "firstQuaterSales": row[4],
            "secondQuaterQty": row[5],  
            "secondQuaterSales": row[6],
            "thirdQuaterQty": row[7],
            "thirdQuaterSales": row[8],
            "fourthQuaterQty": row[9],
            "fourthQuaterSales": row[10],
            "total": row[11],   
        }
        serialized_rows.append(serialized_row)
    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    ret = get_pagination(
        "/quarterly_sales_report",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@report_router.get("/best_product_given_time/search")
def get_best_product_given_time(
    date_from: str,
    date_to: str,
    response: Response,
    request: Request,
    page_num: int = 1,
    page_size: int = 10,
):

    # TODO add field validation

    start = (page_num - 1) * page_size
    sql_query_str = "SELECT po.sku, pv.name, sum(po.quantity) AS sales_count \
        FROM product_variant pv \
        JOIN product_order po ON po.sku = pv.sku\
        JOIN order_cart oc ON oc.order_id = po.order_id\
        WHERE oc.billing_date BETWEEN '{}' AND '{}' \
        GROUP BY po.sku \
        ORDER BY sales_count DESC \
        LIMIT {} OFFSET {}".format(
        date_from,
        date_to,
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
            "sales_count": row[2],
        }
        serialized_rows.append(serialized_row)
    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    ret = get_pagination(
        "/best_product_given_time",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@report_router.get("/product_category_with_most_orders")
def get_product_category_with_most_orders(
    response: Response,
    request: Request,
    page_num: int = 1,
    page_size: int = 10,
):

    # TODO add field validation

    start = (page_num - 1) * page_size
    sql_query_str = "SELECT sc.name, SUM(po.quantity) AS orders_count \
        FROM sub_category sc\
        JOIN product_sub_category psc ON psc.subcategory_id = sc.id\
        JOIN  product p ON p.id = psc.product_id \
        JOIN  product_variant pv ON pv.product_id = p.id \
        JOIN  product_order po ON po.sku = pv.sku\
        GROUP BY sc.name \
        ORDER BY orders_count DESC\
        LIMIT {} OFFSET {}".format(
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
            "name": row[0],
            "orders_count": row[1],
        }
        serialized_rows.append(serialized_row)
    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    ret = get_pagination(
        "/product_category_with_most_orders",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@report_router.get("/product_most_interested_time/search")
def get_product_most_interested_time(
    sku: str,
    response: Response,
    request: Request,
    page_num: int = 1,
    page_size: int = 10,
):

    # TODO add field validation

    start = (page_num - 1) * page_size
    sql_query_str = "SELECT po.sku, po.price, po.quantity, date_format(oc.billing_date,'%M') AS month\
        FROM order_cart oc \
        JOIN product_order po ON oc.order_id = po.id\
        WHERE po.sku = '{}' AND oc.billing_date BETWEEN DATE_SUB( now(), INTERVAL 12 MONTH ) AND now() \
        GROUP BY month\
        LIMIT {} OFFSET {}".format(
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

    total_rows = 5  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = []
    for row in rows:
        serialized_row = {
            "sku": row[0],
            "price": row[1],
            "quantity": row[2],
            "month": row[3],
        }
        serialized_rows.append(serialized_row)
    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    ret = get_pagination(
        "/custormer_orders",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@report_router.get("/customer_orders")
def get_custormer_orders(
    response: Response,
    request: Request,
    page_num: int = 1,
    page_size: int = 10,
):

    # TODO add field validation

    start = (page_num - 1) * page_size
    sql_query_str = "SELECT user.id as userId, po.id as productOrderId, oc.billing_date, po.sku, po.price, po.quantity\
        FROM user \
        JOIN order_cart oc ON oc.order_id = user.id\
        JOIN product_order po ON po.id = oc.order_id\
        ORDER BY oc.billing_date DESC\
        LIMIT {} OFFSET {}".format(
        page_size,
        start,
    )

    cnx = connection_pool.get_connection()
    cursor = cnx.cursor()
    cursor.execute(sql_query_str)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    total_rows = 10 # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = []
    for row in rows:
        serialized_row = {
            "userId": row[0],
            "productOrderId": row[1],
            "billing_date": row[2],
            "sku": row[3],
            "price": row[4],
            "quantity": row[5],
        }
        serialized_rows.append(serialized_row)
    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    ret = get_pagination(
        "/customer_orders",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret
