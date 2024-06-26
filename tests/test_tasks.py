import pytest
from httpx import AsyncClient


async def test_create_task(ac: AsyncClient, new_task):
    response = await ac.post("/v1/tasks/", json=new_task)
    assert response.status_code == 200
