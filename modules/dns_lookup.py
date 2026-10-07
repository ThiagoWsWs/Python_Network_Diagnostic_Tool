import socket

from modules.validators import is_valid_host


def _reverse_lookup(ip_address):
    """Return the hostname for an IP address, or None if not available."""
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except OSError:
        # socket.herror and socket.gaierror are both subclasses of OSError
        return None


def dns_lookup(domain):
    """Resolve a domain and return a dictionary:

    {
        "success": bool,
        "domain": str,
        "ipv4": [str, ...],
        "ipv6": [str, ...],
        "hostname": str or None,   # reverse DNS of the first IP found
        "error": str or None,
    }
    """
    domain = domain.strip()

    if not is_valid_host(domain):
        return {
            "success": False,
            "domain": domain,
            "ipv4": [],
            "ipv6": [],
            "hostname": None,
            "error": "Invalid domain. Enter a valid domain name or IP address.",
        }

    try:
        infos = socket.getaddrinfo(domain, None)

    except socket.gaierror:
        return {
            "success": False,
            "domain": domain,
            "ipv4": [],
            "ipv6": [],
            "hostname": None,
            "error": "DNS lookup failed. Invalid domain or network issue.",
        }

    except Exception as error:
        return {
            "success": False,
            "domain": domain,
            "ipv4": [],
            "ipv6": [],
            "hostname": None,
            "error": f"Error: {error}",
        }

    ipv4 = sorted({info[4][0] for info in infos if info[0] == socket.AF_INET})
    ipv6 = sorted({info[4][0] for info in infos if info[0] == socket.AF_INET6})

    first_ip = (ipv4 or ipv6)[0] if (ipv4 or ipv6) else None
    hostname = _reverse_lookup(first_ip) if first_ip else None

    return {
        "success": True,
        "domain": domain,
        "ipv4": ipv4,
        "ipv6": ipv6,
        "hostname": hostname,
        "error": None,
    }
