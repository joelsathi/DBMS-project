from fastapi import FastAPI, Response
from .auth.routes import user_router
from .core.db import connection
from .core.manager import BaseQueryManager

app = FastAPI()
app.include_router(user_router)


@app.on_event("startup")
async def on_startup():
    BaseQueryManager.set_connection(connection)


@app.on_event("shutdown")
async def on_shutdown():
    connection.close()


# temporary routes
@app.get("/about")
def get_about(response: Response):
    return {"project_name": "Thulasi", "description": "Some Description"}
