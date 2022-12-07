from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/")
def get_root(response: Response):
    return "Hello World"


@app.get("/about")
def get_about(response: Response):
    return {"project_name": "Thulasi", "description": "Some Description"}
