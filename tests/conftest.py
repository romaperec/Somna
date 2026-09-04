import pytest
import pytest_asyncio
from fakeredis.aioredis import FakeRedis
from httpx import ASGITransport, AsyncClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.db_helper import db_helper
from app.core.base import Base
from app.main import app
from app.modules.auth.dependencies import get_auth_redis_client
from app.modules.users.dependencies import get_cache_redis_client

engine = create_async_engine("sqlite+aiosqlite:///file::memory:?cache=shared&uri=true", echo=False, poolclass=StaticPool, connect_args={"check_same_thread": False})
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


fake_cache_redis = FakeRedis(db=0, decode_responses=True)
fake_auth_redis = FakeRedis(db=1, decode_responses=True)

async def override_get_auth_redis():
    return fake_auth_redis

async def override_get_cache_redis():
    return fake_cache_redis

app.dependency_overrides[db_helper.session_getter] = override_get_db
app.dependency_overrides[get_auth_redis_client] = override_get_auth_redis
app.dependency_overrides[get_cache_redis_client] = override_get_cache_redis

@pytest_asyncio.fixture
def user_payload():
    return {
        "username": "test_user",
        "email": "test@email.com",
        "password": "TestPassword123!",
    }

@pytest_asyncio.fixture
async def registered_user(client, user_payload):
    response = await client.post("/auth/register", json=user_payload)
    assert response.status_code == 201
    return user_payload

@pytest_asyncio.fixture
async def auth_client(client, registered_user):
    login_response = await client.post("/auth/login", json={"email": registered_user["email"], "password": registered_user["password"]})
    assert login_response.status_code == 200

    tokens = login_response.json()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers={"Authorization": f"Bearer {tokens['access_token']}"}) as auth_ac:
        yield auth_ac

@pytest_asyncio.fixture
async def client():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(autouse=True)
async def clean_redis():
    await fake_auth_redis.flushall()
    await fake_cache_redis.flushall()
    yield
    await fake_auth_redis.flushall()
    await fake_cache_redis.flushall()