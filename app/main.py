from fastapi import FastAPI

# Router with all /todos endpoints
from app.api.v1.routes.todo import router as todo_router

app = FastAPI()

# Register the router that contains all the /todos endpoints.
app.include_router(todo_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
