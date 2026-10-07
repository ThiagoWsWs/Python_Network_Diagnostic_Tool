# ping_test.py

import platform
import re
import subprocess

from modules.validators import is_valid_host

# Matches "time=12.3 ms", "time<1ms" (Windows) and "tempo=12ms" (Portuguese Windows)
_TIME_PATTERN = re.compile(r"(?:time|tempo)\s*[=<]\s*([\d.,]+)\s*ms", re.IGNORECASE)


def _build_result(success, output="", average_ms=None, error=None):
    return {
        "success": success,
        "output": output,
        "average_ms": average_ms,
        "error": error,
    }


def _extract_average(output):
    """Calculate the average latency from every reply line in the ping output."""
    times = []

    for value in _TIME_PATTERN.findall(output):
        try:
            times.append(float(value.replace(",", ".")))
        except ValueError:
            continue

    if not times:
        return None

    return round(sum(times) / len(times), 1)


def ping_host(host, count=4, timeout=None):
    """Ping a host and return a dictionary:

    {
        "success": bool,        # True if at least one reply was received
        "output": str,          # raw output of the ping command
        "average_ms": float,    # average latency, or None
        "error": str,           # error message, or None
    }
    """
    host = host.strip()

    if not is_valid_host(host):
        return _build_result(False, error="Invalid host. Enter a valid IP address or domain.")

    if timeout is None:
        timeout = count * 5 + 5

    count_flag = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", count_flag, str(count), host]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
        )

    except FileNotFoundError:
        return _build_result(False, error="The 'ping' command was not found on this system.")

    except subprocess.TimeoutExpired:
        return _build_result(False, error="Ping timed out.")

    except OSError as error:
        return _build_result(False, error=f"Error: {error}")

    output = (completed.stdout or completed.stderr).strip()
    average = _extract_average(output)

    # On Windows the exit code can be 0 even for "Destination host unreachable",
    # so we also require at least one real reply (a latency value).
    if completed.returncode == 0 and average is not None:
        return _build_result(True, output, average)

    return _build_result(False, output, error="Host unreachable or request timed out.")
