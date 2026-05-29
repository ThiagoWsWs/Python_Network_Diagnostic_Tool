# ping_test.py

import subprocess
import platform

def ping_host(host):
    try:
        system = platform.system().lower()

        if system == "windows":
            command = ["ping", "-n", "4", host]
        else:
            command = ["ping", "-c", "4", host]

        result = subprocess.run(command, capture_output=True, text=True)

        return result.stdout

    except Exception as error:
        return f"Error: {error}"