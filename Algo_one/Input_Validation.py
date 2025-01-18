import socket  #checking if the target host is reachable by resolving its hostname.
import re      #The regular expressions module, used for validating the port range format.


# Validate the target host
def validate_target(target):
    try:
        # Check if the target is a valid IP or resolves to a domain
        socket.gethostbyname(target)
        return True
    except socket.error:
        print(f"Error: Unable to resolve target '{target}'. Ensure you have an internet connection and a valid IP or domain (e.g., example.com or 110.886.0.8).")
        return False

def validate_port_range(port_range):
    port_pattern = re.compile(r"^(\d+)-(\d+)$")
    match = port_pattern.match(port_range)

    if not match:
        print("Error: Invalid port range format. Use the format 'start-end' (e.g., 20-80).")
        return False

    start_port, end_port = map(int, match.groups())
    if start_port < 1 or end_port > 65535 or start_port > end_port:  #checking if the port range is within the valid range of 1-65535 and if the start port is less than or equal to the end port.

        print("Error: Port range must be between 1-65535 and 'start' <= 'end'.")
        return False

    return True