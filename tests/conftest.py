import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, get_session
from models import RoverState
from schemas import Direction


# Use in-memory SQLite database for testing
@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(engine, session):
    # Override the get_session dependency to use the test database
    def get_test_session():
        yield session

    app.dependency_overrides[get_session] = get_test_session

    # Initialize rover state for testing
    rover_state = RoverState(
        id=1,
        longitude=0,
        latitude=0,
        direction=Direction.NORTH,
    )
    session.add(rover_state)
    session.commit()

    # Create test client
    client = TestClient(app)
    yield client

    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture(name="test_obstacles")
def test_obstacles_fixture():
    return [(5, 5), (10, 10)]