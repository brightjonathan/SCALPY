import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def detect_service(target, open_ports):
    service_info = {}

    print("\nDetecting services on open ports...")

    def check_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)  # Set timeout to 3 seconds
                sock.connect((target, port))
                
                # Send a basic request to get a response
                sock.sendall(b'\n')
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()

                return port, banner if banner else "Unknown Service"
        except (socket.timeout, socket.error) as e:
            return port, f"Error: {e}"

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_port = {executor.submit(check_port, port): port for port in open_ports}
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                port, service = future.result()
                service_info[port] = service
                print(f"Port {port}: {service_info[port]}")
            except Exception as e:
                print(f"Port {port} generated an exception: {e}")

    return service_info