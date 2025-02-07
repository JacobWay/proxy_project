import socket
import threading
from proxy.request_handler import handle_client

# Configuration
HOST: str = '127.0.0.1'  # Proxy server address
PORT: int = 7777         # Proxy server port

def start_proxy():
    server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Proxy server listening on {HOST}:{PORT}")
    
    while True:
        client_socket: socket.socket
        addr: tuple[str, int]
        client_handler: threading.Thread
        
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy()