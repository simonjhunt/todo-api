from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.engine import engine
from app.models.todo import ToDoDB
from app.api.v1.routes.todo import router as todo_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    ToDoDB.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

# Register the router
app.include_router(todo_router)


# Optional health‑check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
