import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# The concurrent.futures module provides a high-level interface for asynchronously executing functions in threads or processes. it speeds up the port scanning process by running multiple threads concurrently.

# Port scanning function
def scan_port(target, port, timeout, verbose, protocol='TCP'):
    try:
        if protocol == 'TCP':
            sock_type = socket.SOCK_STREAM
        elif protocol == 'UDP':
            sock_type = socket.SOCK_DGRAM
        else:
            raise ValueError("Unsupported protocol. Use 'TCP' or 'UDP'.")

        with socket.socket(socket.AF_INET, sock_type) as sock:
            sock.settimeout(timeout)
            if protocol == 'TCP':
                result = sock.connect_ex((target, port))
                if result == 0:
                    if verbose:
                        print(f"Port {port} is open (TCP)")
                    return port
            elif protocol == 'UDP':
                try:
                    sock.sendto(b'', (target, port))
                    sock.recvfrom(1024)
                    if verbose:
                        print(f"Port {port} is open (UDP)")
                    return port
                except socket.error:
                    pass
    except socket.error as e:
        if verbose:
            print(f"Error scanning port {port}: {e}")
    return None

def perform_port_scanning(target, port_range, timeout=1, verbose=True, max_workers=100, protocol='TCP'):
    start_port, end_port = map(int, port_range.split('-'))
    open_ports = []

    if verbose:
        print(f"Scanning target: {target} on ports {start_port}-{end_port} using {protocol}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scan_port, target, port, timeout, verbose, protocol) for port in range(start_port, end_port + 1)]
        for future in as_completed(futures):
            port = future.result()
            if port is not None:
                open_ports.append(port)

    return open_ports

# ***** CODE SUMMARY ***** #
# This code LOGIC provides a simple yet effective way to scan a range of ports on a given target. It utilizes multithreading to speed up the process, allowing multiple ports to be scanned simultaneously. The results include only those ports that are open, and detailed output is controlled by the verbose parameter. The protocol (TCP or UDP) can be specified for the scan. #