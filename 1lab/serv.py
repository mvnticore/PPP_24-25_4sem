import os
import json
import asyncio
import struct


current_root = os.getcwd()


def get_directory_structure(root_dir):
    dir_structure = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        rel_path = os.path.relpath(dirpath, root_dir)
        dir_structure[rel_path] = {
            "directories": dirnames,
            "files": filenames
        }
    return dir_structure


async def handle_client(reader, writer):
    """
    Асинхронная функция для обработки запросов от клиента.
    Поддерживаются команды:
    - SET_ROOT: <путь> – смена корневой директории.
    - GET_STRUCTURE – получение файла с информацией о структуре директории.
    """
    global current_root
    addr = writer.get_extra_info('peername')
    print(f"Подключен клиент: {addr}")
    while True:
        try:
            data = await reader.read(1024)
            if not data:
                break
            command = data.decode().strip()
            print(f"Получена команда: {command} от {addr}")

            if command.startswith("SET_ROOT:"):
                new_root = command[len("SET_ROOT:"):].strip()
                if os.path.isdir(new_root):
                    current_root = new_root
                    response = "Новая корневая директория установлена."
                else:
                    response = "Указанная директория не существует."
                writer.write(response.encode())
                await writer.drain()

            elif command == "GET_STRUCTURE":
                structure = get_directory_structure(current_root)
                json_data = json.dumps(structure, ensure_ascii=False, indent=4)

                with open("directory_structure.json", "w", encoding="utf-8") as f:
                    f.write(json_data)

                encoded_data = json_data.encode("utf-8")
                data_length = len(encoded_data)
                writer.write(struct.pack("!I", data_length))
                writer.write(encoded_data)
                await writer.drain()

            else:
                response = "Неизвестная команда."
                writer.write(response.encode())
                await writer.drain()
        except Exception as e:
            print("Ошибка:", e)
            break

    print(f"Отключение клиента: {addr}")
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Сервер запущен на {addr}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Сервер остановлен.")
