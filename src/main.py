from fastapi import FastAPI

from api_v1 import router as api_v1_router


app = FastAPI(title="tasks and docker")
app.include_router(api_v1_router)
