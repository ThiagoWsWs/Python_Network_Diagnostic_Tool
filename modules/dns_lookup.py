import socket

def dns_lookup(domain):
    try:
        ip_address = socket.gethostbyname(domain)

        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            hostname = "Reverse DNS not available"

        return f"""
=== DNS LOOKUP RESULT ===

Domain: {domain}
IP Address: {ip_address}
Hostname: {hostname}
"""

    except socket.gaierror:
        return "DNS lookup failed. Invalid domain or network issue."

    except Exception as error:
        return f"Error: {error}"