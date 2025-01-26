import socket
import ssl
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate

def scan_port(target, port, timeout, protocol='TCP'):
    """
    Check if a port is open on a target machine using the specified protocol.
    
    Args:
        target (str): The target IP address or hostname.
        port (int): The port number to check.
        protocol (str): The protocol to use ('TCP' or 'UDP').
        timeout (int, optional): The timeout for the socket connection. Default is 1 second.
    
    Returns:
        bool: True if the port is open, False otherwise.
    """
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
                    return True
            elif protocol == 'UDP':
                try:
                    sock.sendto(b'', (target, port))
                    sock.recvfrom(1024)
                    return True
                except socket.error:
                    return False
    except (socket.timeout, socket.error):
        return False
    return False

# Service detection functionality 
# ALGORITHM THREE
def detect_service(target, open_ports):
    service_info = []

    def check_port(port, protocol):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == 'TCP' else socket.SOCK_DGRAM) as sock:
                sock.settimeout(5)  # Set timeout to 5 seconds

                # Wrap SSL for encrypted services
                if protocol == 'TCP' and port in {443, 465, 993, 995}:
                    context = ssl.create_default_context()
                    sock = context.wrap_socket(sock, server_hostname=target)

                if protocol == 'TCP':
                    sock.connect((target, port))
                else:
                    sock.sendto(b'\n', (target, port))
                    sock.recvfrom(1024)

                # Service-specific probing
                if port in {80, 8080}:  # HTTP probing
                    sock.sendall(b'HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n')
                elif port == 25:  # SMTP probing
                    sock.sendall(b'HELO example.com\r\n')

                # Receive banner
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()

                # Attempt to identify the service based on the banner
                service = identify_service(port, banner)
                return port, protocol, service, banner if banner else "Unknown Banner"
        except (socket.timeout, socket.error) as e:
            return port, protocol, "Error", f"Error: {e}"

    def identify_service(port, banner):
        """
        Identify a service based on port number or banner content.

        Args:
            port (int): Port number.
            banner (str): Banner or response string.

        Returns:
            str: Detected service name.
        """
        # Standard port-to-service mappings
        port_service_map = {
            20: "FTP (Data Transfer)",
            21: "FTP (Control)",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            69: "TFTP",
            80: "HTTP",
            110: "POP3",
            123: "NTP",
            143: "IMAP",
            161: "SNMP",
            194: "IRC",
            443: "HTTPS",
            445: "SMB",
            465: "SMTPS",
            514: "Syslog",
            993: "IMAPS",
            995: "POP3S",
            1080: "SOCKS Proxy",
            1433: "MSSQL",
            1521: "Oracle DB",
            1723: "PPTP VPN",
            1883: "MQTT",
            2049: "NFS",
            2375: "Docker API (Unsecured)",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5672: "RabbitMQ",
            6379: "Redis",
            8080: "HTTP Proxy",
            8443: "HTTPS Proxy",
            8888: "Web Application Debugging",
            9200: "Elasticsearch",
            27017: "MongoDB",
        }

        # Regex patterns for banner detection
        banner_patterns = [
            (r"SMTP", "SMTP"),
            (r"POP3", "POP3"),
            (r"IMAP", "IMAP"),
            (r"HTTP\/\d\.\d", "HTTP"),
            (r"HTTPS", "HTTPS"),
            (r"SSH-", "SSH"),
            (r"FTP", "FTP"),
            (r"SMB", "SMB"),
            (r"MySQL", "MySQL"),
            (r"PostgreSQL", "PostgreSQL"),
            (r"MongoDB", "MongoDB"),
            (r"Redis", "Redis"),
            (r"Elasticsearch", "Elasticsearch"),
            (r"RabbitMQ", "RabbitMQ"),
            (r"Docker", "Docker API"),
            (r"Telnet", "Telnet"),
            (r"Oracle", "Oracle DB"),
            (r"RDP", "Remote Desktop Protocol"),
            (r"MQTT", "MQTT"),
        ]

        # Match port to known service
        if port in port_service_map:
            return port_service_map[port]

        # Match banner to known service using regex
        for pattern, service in banner_patterns:
            if re.search(pattern, banner):
                return service

        # Default to unknown if no match is found
        return "Unknown Service"

    # Increase the number of worker threads to speed up the detection
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_port = {executor.submit(check_port, port, protocol): (port, protocol) for port, protocol in open_ports}
        for future in as_completed(future_to_port):
            port, protocol, service, banner = future.result()
            service_info.append((port, protocol, service, banner))

    # Print the results in a tabular form
    headers = ["Port", "Protocol", "Service", "Banner"]
    print(tabulate(service_info, headers=headers, tablefmt="grid"))

def main(target, ports, timeout=1, verbose=False):
    """
    Scan a list of ports on a target machine to check if they are open.
    
    Args:
        target (str): The target IP address or hostname.
        ports (list): A list of port numbers to scan.
        timeout (int, optional): The timeout for each port scan. Default is 1 second.
        verbose (bool, optional): If True, print the status of each port. Default is False.
    
    Returns:
        list: A list of tuples with open ports and their protocols.
    """
    open_ports = []

    # Scan ports for both TCP and UDP
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_port = {executor.submit(scan_port, target, port, timeout, protocol): (port, protocol) for port in ports for protocol in ['TCP', 'UDP']}
        for future in as_completed(future_to_port):
            port, protocol = future_to_port[future]
            if future.result():
                open_ports.append((port, protocol))
                if verbose:
                    print(f"Port {port}/{protocol} is open")

    # Detect services on open ports
    detect_service(target, open_ports)
    return open_ports