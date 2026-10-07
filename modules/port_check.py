import socket

from modules.validators import is_valid_host, is_valid_port


def get_service_name(port):
    """Return the common service name for a TCP port (e.g. 80 -> 'http'), or None."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return None


def check_port(host, port, timeout=3):
    """Check whether a TCP port is open and return a dictionary:

    {
        "success": bool,      # True if the check ran (even if the port is closed)
        "host": str,
        "port": int,
        "is_open": bool,      # True if the connection was accepted
        "service": str,       # common service name, or None
        "error": str,         # error message, or None
    }
    """
    host = host.strip()

    result = {
        "success": False,
        "host": host,
        "port": port,
        "is_open": False,
        "service": None,
        "error": None,
    }

    if not is_valid_host(host):
        result["error"] = "Invalid host. Enter a valid IP address or domain."
        return result

    if not is_valid_port(port):
        result["error"] = "Invalid port. Use a number between 1 and 65535."
        return result

    try:
        # 'with' guarantees the socket is closed, even if an error happens
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            # Timeout to avoid freezing
            client.settimeout(timeout)
            connection_code = client.connect_ex((host, port))

    except socket.gaierror:
        result["error"] = "Could not resolve the host name."
        return result

    except OSError as error:
        result["error"] = f"Error: {error}"
        return result

    result["success"] = True
    result["is_open"] = connection_code == 0
    result["service"] = get_service_name(port)

    return result
