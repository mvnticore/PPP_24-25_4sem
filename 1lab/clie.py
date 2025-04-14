import asyncio
import struct


async def send_command(command):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    writer.write(command.encode())
    await writer.drain()

    if command.startswith("GET_STRUCTURE"):
        data_length_bytes = await reader.readexactly(4)
        data_length = struct.unpack("!I", data_length_bytes)[0]
        data = await reader.readexactly(data_length)
        json_data = data.decode("utf-8")
        print("Структура директории:")
        print(json_data)
    else:
        response = await reader.read(1024)
        print("Ответ сервера:", response.decode())

    writer.close()
    await writer.wait_closed()


async def main():
    while True:
        print("\nВведите команду:")
        print("1. Установить новую корневую директорию: SET_ROOT: <путь>")
        print("2. Получить структуру директории: GET_STRUCTURE")
        print("3. Выход")
        cmd = input("Команда: ")
        if cmd.strip() == "3":
            break
        await send_command(cmd.strip())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Клиент остановлен.")
