import socket

import requests

from modules.validators import is_valid_ip

# Services tried in order until one of them answers
PUBLIC_IP_SERVICES = [
    "https://api.ipify.org",
    "https://ifconfig.me/ip",
    "https://icanhazip.com",
]


def get_local_ip():
    """Return the local IP used to reach the internet:

    {"success": bool, "ip": str or None, "error": str or None}
    """
    try:
        # Create a temporary socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Doesn't actually send traffic to Google,
            # just determines which interface would be used
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]

        return {"success": True, "ip": local_ip, "error": None}

    except OSError as error:
        return {
            "success": False,
            "ip": None,
            "error": f"Error getting local IP: {error}",
        }


def get_public_ip(timeout=5):
    """Return the public IP, trying several services:

    {"success": bool, "ip": str or None, "source": str or None, "error": str or None}
    """
    for service in PUBLIC_IP_SERVICES:
        try:
            response = requests.get(service, timeout=timeout)
            response.raise_for_status()

            public_ip = response.text.strip()

            # Make sure the service really returned an IP address
            if is_valid_ip(public_ip):
                return {
                    "success": True,
                    "ip": public_ip,
                    "source": service,
                    "error": None,
                }

        except requests.RequestException:
            continue

    return {
        "success": False,
        "ip": None,
        "source": None,
        "error": "Error getting public IP: no service responded. Check your connection.",
    }
