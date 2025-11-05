import psutil
from . import utils

def get_open_ports():
    """Returns a dictionary of open ports and their processes."""
    try:
        connections = psutil.net_connections(kind='inet')
    except PermissionError:
        utils.print_danger("Permission denied. Try running with sudo or as root.")
        return {}
    open_ports = {}
    for conn in connections:
        if conn.status == 'LISTEN' and conn.laddr.port not in open_ports:
            try:
                proc = psutil.Process(conn.pid)
                open_ports[conn.laddr.port] = {
                    "pid": conn.pid,
                    "process": proc.name(),
                    "user": proc.username(),
                    "protocol": "TCP" if conn.type == 1 else "UDP",
                    "address": f"{conn.laddr.ip}:{conn.laddr.port}",
                    "family": "IPv4" if conn.family == 2 else "IPv6"
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Ignore processes that have already terminated or we don't have access to
                continue
    return open_ports

def scan():
    """Scans for open ports and prints them in a table."""
    utils.print_info("Scanning for open ports...")
    open_ports = get_open_ports()
    if not open_ports:
        utils.print_success("No open ports found.")
        return

    headers = ["Port", "Process", "PID", "User", "Protocol", "Address", "Family"]
    rows = []
    for port, info in sorted(open_ports.items()):
        rows.append([
            port,
            info["process"],
            info["pid"],
            info["user"],
            info["protocol"],
            info["address"],
            info["family"]
        ])
    utils.print_table(headers, rows)
