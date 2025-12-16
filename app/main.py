from contextlib import asynccontextmanager
from fastapi import FastAPI

# Router with all /todos endpoints
from app.api.v1.routes.todo import router as todo_router

# Import the lazy factory and metadata
from app.db.engine import get_engine, metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs once when the app starts.  Because we call `get_engine()` *here*,
    the engine is built **after** any test fixture may have patched
    `settings`.  The same engine is then used by the request‑scoped
    `get_session` dependency.
    """
    # 2️⃣ Build the engine *now* – it will respect the current settings
    engine = get_engine()

    # 3️⃣ Create tables synchronously on that engine
    metadata.create_all(bind=engine)

    # Yield control back to FastAPI – the app is ready
    yield

    # (Optional) graceful‑shutdown logic could go here


app = FastAPI(lifespan=lifespan)

# Register the router that contains all the /todos endpoints.
app.include_router(todo_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
