import socket

def extract_target_host(request: bytes) -> tuple[str, int]:
    lines: list[str] = request.decode(errors='ignore').split('\r\n')
    target_host: str | None = None
    target_port: int = 80  # Default HTTP port
    
    for line in lines:
        if line.lower().startswith("host:"):
            target_host = line.split(": ")[1]
            if ':' in target_host:
                host, port = target_host.split(':')
                return host, int(port)
            return target_host, target_port
    return None, None

def handle_client(client_socket: socket.socket):
    request: bytes = client_socket.recv(4096)
    print(f"Received request: {request.decode(errors='ignore')}")
    
    target_host, target_port = extract_target_host(request)
    if not target_host:
        print("[!] Could not determine target host.")
        client_socket.close()
        return
    
    remote_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((target_host, target_port))
    remote_socket.sendall(request)
    
    response: bytes = remote_socket.recv(4096)
    print("Forwarding response to client...")
    client_socket.sendall(response)
    
    remote_socket.close()
    client_socket.close()