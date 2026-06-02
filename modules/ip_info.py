import socket
import requests


def get_local_ip():
    try:
        # Create a temporary socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Doesn't actually send traffic to Google,
        # just determines which interface would be used
        s.connect(("8.8.8.8", 80))

        local_ip = s.getsockname()[0]

        s.close()

        return f"""
=== LOCAL IP INFORMATION ===

Local IP: {local_ip}
"""

    except Exception as error:
        return f"Error getting local IP: {error}"


def get_public_ip():
    try:
        response = requests.get(
            "https://api.ipify.org",
            timeout=5
        )

        public_ip = response.text

        return f"""
=== PUBLIC IP INFORMATION ===

Public IP: {public_ip}
"""

    except Exception as error:
        return f"Error getting public IP: {error}"