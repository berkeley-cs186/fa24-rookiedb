"""
A client for connecting to a RookieDB server.
See src/main/java/edu/berkeley/cs186/database/cli/Server.java
for details
"""
import socket
import threading
import sys
import argparse

DEFAULT_PORT = 18600
DEFAULT_HOST = "localhost"


def receive(s):
    while True:
        data = s.recv(1024)
        if len(data) == 0:
            break
        print(data.decode("utf-8"), end="")
        sys.stdout.flush()


def main(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    receive_thread = threading.Thread(target=receive, args=(s,))
    receive_thread.start()

    try:
        while True:
            inp = input()
            if inp.replace(";", "").strip().lower() == "exit":
                break
            s.send((inp + "\n").encode("utf-8"))
    except (EOFError, KeyboardInterrupt):
        # User sent ctrl+D or ctrl+C
        print("exit")
    finally:
        s.shutdown(socket.SHUT_RDWR)
        s.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect to a RookieDB server.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", "-p", default=DEFAULT_PORT, type=int)
    args = parser.parse_args()
    main(args.host, args.port)
