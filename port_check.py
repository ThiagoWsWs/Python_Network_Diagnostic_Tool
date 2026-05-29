import socket

def check_port(host, port):
    try:
        # Create socket object
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Timeout to avoid freezing
        client.settimeout(3)

        # Try connection
        result = client.connect_ex((host, port))

        client.close()

        if result == 0:
            return f"\nPort {port} is OPEN on {host}"

        else:
            return f"\nPort {port} is CLOSED on {host}"

    except Exception as error:
        return f"\nError: {error}"