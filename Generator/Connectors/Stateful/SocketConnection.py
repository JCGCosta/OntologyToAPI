import socket as soc

class SocketConnection:
    def __init__(self, args):
        try:
            self.socket = soc.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((args["hasHost"], args["hasPort"]))
        except Exception as e:
            print("Connection failed:", e)

    def exec_query(self, message: str):
        try:
            self.socket.sendall(message.encode())
            return self.socket.recv(8192).decode()
        except Exception as e:
            return {'error': str(e)}