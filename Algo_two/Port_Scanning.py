import socket;
from concurrent.futures import ThreadPoolExecutor, as_completed;
#The concurrent.futures module provides a high-level interface for asynchronously executing functions in threads or processes. it speeds up the port scanning process by running multiple threads concurrently.


#Port scanning function
def scan_port(target, port, timeout, verbose):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            if result == 0:
                if verbose:
                    print(f"Port {port} is open")
                return port
    except socket.error as e:
        if verbose:
            print(f"Error scanning port {port}: {e}")
    return None

def perform_port_scanning(target, port_range, timeout=1, verbose=True, max_workers=100):
    start_port, end_port = map(int, port_range.split('-'))
    open_ports = []

    if verbose:
        print(f"Scanning target: {target} on ports {start_port}-{end_port}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scan_port, target, port, timeout, verbose) for port in range(start_port, end_port + 1)]
        for future in as_completed(futures):
            port = future.result()
            if port is not None:
                open_ports.append(port)

    return open_ports


# ***** CODE SUMMARY ***** #
# This code LOGIC  provides a simple yet effective way to scan a range of ports on a given target. It utilizes multithreading to speed up the process, allowing multiple ports to be scanned simultaneously. The results include only those ports that are open, and detailed output is controlled by the verbose parameter. #