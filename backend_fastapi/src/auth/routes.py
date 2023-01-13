import json
from fastapi import APIRouter, Response, status, Request, HTTPException, Header, Form

from .models import RegisteredUserDBModel, UserDBModel, PaymentDetailDBModel

from ..core.pagination import get_pagination, get_params

from .utils import (
    get_password_hash,
    encode_token,
    decode_token,
    verify_password,
    checkAdmin,
    checkCustomer,
)
from fastapi.responses import JSONResponse

from ..core.db import connection_pool


user_router = APIRouter(
    prefix="/auth",
)


@user_router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):

    cnx = connection_pool.get_connection()
    cursor = cnx.cursor()

    query = "SELECT password, is_admin, id FROM registered_user WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()

    if result:
        hashed_password, is_admin, id = result

        # Perform authentication and authorization here
        if verify_password(plain_password=password, hashed_password=hashed_password):
            # for Authorization
            role = "customer"
            if is_admin:
                role = "admin"
            payload = {"username": username, "role": role, "id": id}

            # Create a JWT token with user information
            token = encode_token(payload=payload)
            return JSONResponse(
                content={
                    "message": "Welcome registered user!",
                    "token": token,
                    "isAdmin": is_admin,
                }
            )
        else:
            return JSONResponse(
                content={"message": "Invalid credentials."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@user_router.get("/secure")
async def secure_route(authorization: str = Header(None, prefix="Bearer ")):
    try:
        # Separate the token from the "Bearer " prefix
        token = authorization.replace("Bearer ", "")
        # Verify the JWT token
        payload = decode_token(token)
        return JSONResponse(content={"message": f"Welcome {payload['username']}!"})
    except:  # noqa
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )


@user_router.get("/registered_user")
# "{BASE_URL}/auth/registered_user?page_num=1&page_size=10&sort_by=id,username&sort_order=ASC,DESC&username=thulasithang"
def get_registered_user_list(
    response: Response,
    request: Request,
):
    checkAdmin(request=request)

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = RegisteredUserDBModel.objects.select(
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

    serialized_rows = [RegisteredUserDBModel.serialize(row) for row in rows]

    ret = get_pagination(
        "/registered_user",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )

    return ret


@user_router.post("/registered_user")
async def post_registered_user(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["password"] = get_password_hash(field_dict["password"])
    new_obj = RegisteredUserDBModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@user_router.get("/registered_user/{id}")
def get_registered_user(id: int, response: Response, request: Request):

    checkCustomer(request=request, id=id)

    row = RegisteredUserDBModel.objects.select_by_id(id)
    if row is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        # TODO create a error response class
        return {
            "Error": "Detail Not Found",
            "Message": "RegisteredUser with id {} not found".format(id),
        }

    return RegisteredUserDBModel.serialize_with_related(row)


@user_router.put("/registered_user/{id}")
async def put_registered_user(id: int, request: Request, response: Response):
    checkCustomer(request=request, id=id)
    field_dict = await request.json()
    field_dict["id"] = id
    if "password" in field_dict:
        field_dict["password"] = get_password_hash(field_dict["password"])
    upd_obj = RegisteredUserDBModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@user_router.delete("/registered_user/{id}")
def delete_registered_user(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = RegisteredUserDBModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


@user_router.get("/user")
def get_user_list(
    response: Response,
    request: Request,
):
    checkAdmin(request=request)

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = UserDBModel.objects.select(
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

    serialized_rows = [UserDBModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/user",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@user_router.post("/user")
async def post_user(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = UserDBModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@user_router.put("/user/{id}")
async def put_user(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = UserDBModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@user_router.delete("/user/{id}")
def delete_user(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = RegisteredUserDBModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


@user_router.get("/payment_detail")
def get_payment_detail_list(
    response: Response,
    request: Request,
):
    checkAdmin(request=request)

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows, total_rows = PaymentDetailDBModel.objects.select(
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

    serialized_rows = [PaymentDetailDBModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/payment_detail",
        total=total_rows,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@user_router.post("/payment_detail")
async def post_payment_detail(request: Request, response: Response):
    checkAdmin(request=request)
    field_dict = await request.json()
    new_obj = PaymentDetailDBModel(**field_dict)
    success = new_obj.save()
    if success:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "success", "id": new_obj.id}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to create"}


@user_router.put("/payment_detail/{id}")
async def put_payment_detail(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    field_dict = await request.json()
    field_dict["id"] = id
    upd_obj = UserDBModel(**field_dict, is_existing=True)
    success = upd_obj.save()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to update"}


@user_router.delete("/payment_detail/{id}")
def delete_payment_detail(id: int, response: Response, request: Request):
    checkAdmin(request=request)
    del_obj = RegisteredUserDBModel(id=id, is_existing=True)
    success = del_obj.remove()
    if success:
        response.status_code = status.HTTP_200_OK
        return {"message": "success"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Failed to delete"}


@user_router.post("/register")
async def create_normal_user(request: Request):
    field_dict = await request.json()
    field_dict["password"] = get_password_hash(field_dict["password"])
    conn = None
    cursor = None
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("START TRANSACTION")
        cursor.execute("CALL create_user(%s)", (json.dumps(field_dict),))
        conn.commit()
        return JSONResponse(content={"message": "User created successfully"})
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
