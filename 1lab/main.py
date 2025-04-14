import subprocess
import time
import sys


def main():
    server_process = subprocess.Popen([sys.executable, 'serv.py'])
    time.sleep(3)
    client_process = subprocess.Popen([sys.executable, 'clie.py'])
    server_process.wait()
    client_process.wait()


if __name__ == '__main__':
    main()
