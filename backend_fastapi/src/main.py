from fastapi import FastAPI, Response
from .auth.routes import user_router
from .product.routes import product_router
from .order.routes import order_router
from .reports.routes import report_router
from .core.db import connection_pool
from .core.manager import BaseQueryManager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

