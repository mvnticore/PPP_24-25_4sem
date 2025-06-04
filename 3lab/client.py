import asyncio
import websockets
import click
import httpx
import json
import os


async def listen_notifications(user_id: str, token: str):
    async with websockets.connect(
            f"ws://localhost:8000/ws/{user_id}",
            extra_headers={"Authorization": f"Bearer {token}"}
    ) as ws:
        print(f"Connected to WebSocket for user {user_id}")
        while True:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=300)
                notification = json.loads(msg)
                print(f"\n[NOTIFICATION] {notification}\n> ", end="")
            except asyncio.TimeoutError:
                print("\nWebSocket connection timed out")
                break


async def login(username: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code != 200:
            raise Exception(f"Login failed: {response.text}")
        return response.json()["access_token"]

async def register(username: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/auth/register",
            json={"username": username, "password": password}
        )
        if response.status_code != 200:
            raise Exception(f"Registration failed: {response.text}")
        return response.json()["access_token"]


async def solve_tsp_command(points: list, token: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/tasks/solve-tsp",
            json={"points": points},
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()


@click.command()
@click.option("--username", prompt="Username")
@click.option("--password", prompt="Password", hide_input=True)
@click.option("--register", is_flag=True, help="Register new user")
def main(username, password, register):
    # Регистрация или аутентификация
    if register:
        token = asyncio.run(register(username, password))
        print(f"User {username} registered successfully")
    else:
        token = asyncio.run(login(username, password))
        print(f"User {username} authenticated successfully")
    user_id = username  # Для простоты используем username как user_id

    # Запускаем прослушивание уведомлений в фоне
    loop = asyncio.get_event_loop()
    listener = asyncio.ensure_future(listen_notifications(user_id, token))

    print("Commands:")
    print("  solve-tsp [[x1,y1],[x2,y2],...] - Start TSP calculation")
    print("  exit - Quit the program")

    try:
        while True:
            command = input("> ")
            if command.startswith("solve-tsp"):
                try:
                    points_str = command.split(" ", 1)[1]
                    points = json.loads(points_str)
                    response = asyncio.run(solve_tsp_command(points, token))
                    print(f"Task started: {response['task_id']}")
                except Exception as e:
                    print(f"Error: {e}")
            elif command == "exit":
                listener.cancel()
                break
            else:
                print("Unknown command")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    main()