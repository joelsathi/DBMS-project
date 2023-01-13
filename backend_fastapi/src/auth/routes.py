from fastapi import APIRouter, Response, status, Request, HTTPException, Header, Form

from .models import RegisteredUserDBModel, UserDBModel, PaymentDetailDBModel

from ..core.pagination import get_pagination, get_params

from .utils import get_password_hash, encode_token, decode_token, verify_password
from fastapi.responses import JSONResponse

from ..core.db import connection


user_router = APIRouter(
    prefix="/auth",
)

@user_router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):

    cursor = connection.cursor()
    
    #### This is for Authorization
    #### query = "SELECT password, role FROM users WHERE username = %s"
    query = "SELECT password FROM registered_user WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        #### hashed_password, role = result
        hashed_password = result[0]

        # password = get_password_hash(password=password)

        # Perform authentication and authorization here
        if verify_password(plain_password=password, hashed_password=hashed_password):
            #### for Authorization
            #### payload = {"username": username, "role": role}

            # Create a JWT token with user information
            payload = {"username": username}
            token = encode_token(payload=payload)
            return JSONResponse(content={"message": "Welcome registered user!", "token": token})
        else:
            return JSONResponse(content={"message": "Invalid credentials."}, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return JSONResponse(content={"message": "Invalid credentials."}, status_code=status.HTTP_401_UNAUTHORIZED)

@user_router.get("/secure")
async def secure_route(authorization: str = Header(None)):
    # Verify the JWT token
    try:
        payload = decode_token(authorization=authorization)
        return JSONResponse(content={"message": f"Welcome {payload['username']}!"})
    except:
        raise HTTPException(status_code=401, detail="Invalid token.")

@user_router.get("/registered_user")
# "{BASE_URL}/auth/registered_user?page_num=1&page_size=10&sort_by=id,username&sort_order=ASC,DESC&username=thulasithang"
def get_registered_user_list(
    response: Response,
    request: Request,
):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = RegisteredUserDBModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = 18  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [RegisteredUserDBModel.serialize(row) for row in rows]

    ret = get_pagination(
        "/registered_user",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )

    return ret

@user_router.post("/registered_user")
async def post_registered_user(request: Request):
    field_dict = await request.json()
    field_dict["password"] = get_password_hash(field_dict["password"])
    new_obj = RegisteredUserDBModel(**field_dict)
    new_obj.save()
    print(new_obj)


@user_router.get("/registered_user/{id}")
def get_registered_user(
    id: int,
    response: Response,
):
    row = RegisteredUserDBModel.objects.select_by_id(id)
    if row is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        # TODO create a error response class
        return {
            "Error": "Detail Not Found",
            "Message": "RegisteredUser with id {} not found".format(id),
        }

    return RegisteredUserDBModel.serialize_with_related(row)


@user_router.get("/user")
def get_user_list(
    response: Response,
    request: Request,
):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = UserDBModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [UserDBModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/user",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret


@user_router.get("/payment_detail")
def get_payment_detail_list(
    response: Response,
    request: Request,
):

    page_num, page_size, sort_dict, where_params = get_params(request.query_params)

    # TODO add field validation

    rows = PaymentDetailDBModel.objects.select_by_all(
        page_num=page_num, page_size=page_size, sort_=sort_dict, filters=where_params
    )

    if rows is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "Error": "Detail not Found",
            "Message": "No entries on page {}".format(page_num),
        }

    total = None  # NEED TO IMPLEMENT THE FUNCTION
    serialized_rows = [PaymentDetailDBModel.serialize(row) for row in rows]
    ret = get_pagination(
        "/payment_detail",
        total=total,
        serialized_rows=serialized_rows,
        page_num=page_num,
        page_size=page_size,
    )
    return ret
