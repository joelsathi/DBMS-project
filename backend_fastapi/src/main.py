from fastapi import FastAPI, Response
from .auth.routes import user_router
from .product.routes import product_router
from .order.routes import order_router
from .reports.routes import report_router
from .core.db import connection_pool
from .core.manager import BaseQueryManager

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(report_router)

@app.on_event("startup")
async def on_startup():
    BaseQueryManager.set_connection_pool(connection_pool)


@app.on_event("shutdown")
async def on_shutdown():
    connection_pool._remove_connections()


# temporary routes
@app.get("/about")
def get_about(response: Response):
    return {"project_name": "Thulasi", "description": "Some Description"}

# added to allow request from frontend
@app.middleware("http")
async def cors_middleware(request, call_next):
    response = await call_next(request)
    # response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    return response
