# tests/test_endpoints.py
import pytest
from fastapi import status

from app.schemas.todo_get import ToDoGet

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.db.session import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# -----------------------------------------------------------------
# Helper: create a todo via the API (returns the parsed ToDoGet model)
# -----------------------------------------------------------------
def api_create_todo(client: TestClient, title: str, description: str) -> ToDoGet:
    payload = {"title": title, "description": description}
    resp = client.post("/todos", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    return ToDoGet(**resp.json())


# -----------------------------------------------------------------
# Health‑check endpoint
# -----------------------------------------------------------------
def test_health(client: TestClient):
    resp = client.get("/health")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"status": "ok"}


# -----------------------------------------------------------------
# Full CRUD cycle via HTTP
# -----------------------------------------------------------------
def test_crud_cycle(client: TestClient):
    client = TestClient(app)

    # ---- CREATE ----
    created = api_create_todo(
        client,
        title="Write integration test",
        description="Cover all endpoints.",
    )
    assert created.id is not None
    assert created.title == "Write integration test"

    # ---- LIST ----
    list_resp = client.get("/todos")
    assert list_resp.status_code == status.HTTP_200_OK
    todos = list_resp.json()
    assert any(t["id"] == created.id for t in todos)

    # ---- GET SINGLE ----
    get_resp = client.get(f"/todos/{created.id}")
    assert get_resp.status_code == status.HTTP_200_OK
    fetched = ToDoGet(**get_resp.json())
    assert fetched.title == created.title

    # ---- UPDATE (mark done) ----
    patch_resp = client.patch(
        f"/todos/{created.id}",
        json={"done": True},
    )
    assert patch_resp.status_code == status.HTTP_200_OK
    updated = ToDoGet(**patch_resp.json())
    assert updated.done is True
    assert updated.completed_at is not None

    # ---- UPDATE (change title) ----
    patch_resp2 = client.patch(
        f"/todos/{created.id}",
        json={"title": "New title"},
    )
    assert patch_resp2.status_code == status.HTTP_200_OK
    updated2 = ToDoGet(**patch_resp2.json())
    assert updated2.title == "New title"
    # done flag should stay true
    assert updated2.done is True

    # ---- DELETE ----
    del_resp = client.delete(f"/todos/{created.id}")
    assert del_resp.status_code == status.HTTP_204_NO_CONTENT

    # Verify it’s gone
    get_after_del = client.get(f"/todos/{created.id}")
    assert get_after_del.status_code == status.HTTP_404_NOT_FOUND


# -----------------------------------------------------------------
# Pagination parameters work as expected
# -----------------------------------------------------------------
def test_pagination(client: TestClient):
    # Create 5 todos
    for i in range(5):
        api_create_todo(
            client,
            title=f"Item {i}",
            description=f"This is description {i}",
        )

    # First page (limit 3)
    resp_page1 = client.get("/todos?offset=0&limit=3")
    assert resp_page1.status_code == status.HTTP_200_OK
    page1 = resp_page1.json()
    assert len(page1) == 3
    assert page1[0]["title"] == "Item 0"

    # Second page (skip first 3)
    resp_page2 = client.get("/todos?offset=3&limit=3")
    assert resp_page2.status_code == status.HTTP_200_OK
    page2 = resp_page2.json()
    assert len(page2) == 2
    assert page2[0]["title"] == "Item 3"
