import httpx
import asyncio
import json


async def test_explain():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/api/v1/explain/",
                json={"code": 'print("hello world")', "language": "python"},
                timeout=30.0,
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")


asyncio.run(test_explain())
