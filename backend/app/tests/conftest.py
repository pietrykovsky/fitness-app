import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

from app.main import app as base_app
from app.core.deps import get_db
from app.core.database import Base
from app.tests import env


@pytest.fixture(scope="session")
def db_engine_session() -> tuple[Engine, sessionmaker]:
    """Provide a test engine and session for the test session."""
    engine = create_engine(
        env.SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine)
    return engine, TestingSessionLocal


@pytest.fixture(scope="function", autouse=True)
def setup_database(db_engine_session: tuple[Engine, sessionmaker]):
    """Set up and tear down the test database."""
    engine, _ = db_engine_session
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine_session: tuple[Engine, sessionmaker]) -> Session:
    """Provide a test database session for CRUD operations."""
    _, TestingSessionLocal = db_engine_session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function", autouse=True)
def override_get_db(db_engine_session: tuple[Engine, sessionmaker]):
    """Override the get_db dependency to use the test database."""
    _, TestingSessionLocal = db_engine_session

    def _get_db_override():
        with TestingSessionLocal() as db:
            yield db

    base_app.dependency_overrides[get_db] = _get_db_override
    yield
    base_app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """Provide the FastAPI app instance."""
    return base_app


@pytest.fixture(scope="session")
def client(app: base_app) -> TestClient:
    """Provide a test client for FastAPI using the provided app instance."""
    with TestClient(app) as c:
        yield c
