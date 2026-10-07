import ipaddress
import platform
import re
import socket
import subprocess

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


# ---------------------------------------------------------------------------
# CGNAT detection
# ---------------------------------------------------------------------------

# Shared address space reserved for CGNAT by ISPs (RFC 6598)
CGNAT_NETWORK = ipaddress.ip_network("100.64.0.0/10")

_HOP_LINE_PATTERN = re.compile(r"^\s*\d+\s+")
_IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def _parse_hops(output):
    """Extract the first IPv4 address of each hop line from a traceroute output."""
    hops = []

    for line in output.splitlines():
        # Only lines that start with the hop number (skips the header line)
        if not _HOP_LINE_PATTERN.match(line):
            continue

        for candidate in _IPV4_PATTERN.findall(line):
            try:
                hops.append(ipaddress.ip_address(candidate))
                break
            except ValueError:
                continue

    return hops


def _trace_first_hops(target="8.8.8.8", max_hops=6, timeout=40):
    """Run traceroute/tracert for the first hops. Returns (hops, error)."""
    if platform.system().lower() == "windows":
        command = ["tracert", "-d", "-h", str(max_hops), "-w", "1000", target]
    else:
        command = ["traceroute", "-n", "-m", str(max_hops), "-w", "1", "-q", "1", target]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
        )

    except FileNotFoundError:
        return [], "The traceroute command was not found on this system."

    except subprocess.TimeoutExpired:
        return [], "Traceroute timed out."

    except OSError as error:
        return [], f"Error: {error}"

    return _parse_hops(completed.stdout), None


def check_cgnat(public_ip=None):
    """Try to detect whether the connection is behind CGNAT.

    It looks at the first network hops between you and the internet:

    {
        "success": bool,     # True if the check could be performed
        "status": str,       # "cgnat", "possible", "no_cgnat", "no_evidence" or "unknown"
        "hops": [str, ...],  # IPs of the first hops
        "evidence": str,     # explanation of the conclusion, or None
        "error": str,        # error message, or None
    }

    This is a heuristic: only comparing your router's WAN IP with the public IP
    gives a 100% certain answer.
    """
    hops, error = _trace_first_hops()

    if error:
        return {"success": False, "status": "unknown", "hops": [], "evidence": None, "error": error}

    if not hops:
        return {
            "success": False,
            "status": "unknown",
            "hops": [],
            "evidence": None,
            "error": "Could not read any hop from the traceroute output.",
        }

    hop_strings = [str(hop) for hop in hops]

    def build(status, evidence):
        return {
            "success": True,
            "status": status,
            "hops": hop_strings,
            "evidence": evidence,
            "error": None,
        }

    # 1) A hop inside 100.64.0.0/10 is the classic sign of CGNAT
    for hop in hops:
        if hop in CGNAT_NETWORK:
            return build(
                "cgnat",
                f"Hop {hop} is in 100.64.0.0/10, the address range reserved for CGNAT.",
            )

    # 2) One of the first hops is your own public IP: your router has it directly
    if public_ip and public_ip in hop_strings:
        return build(
            "no_cgnat",
            f"Your public IP ({public_ip}) appears in the first hops, so it is not shared.",
        )

    # 3) Two or more private hops before reaching a public one: double NAT
    private_hops = 0

    for hop in hops:
        if hop.is_private:
            private_hops += 1
        else:
            break

    if private_hops >= 2:
        return build(
            "possible",
            f"{private_hops} private hops were found before the first public one "
            "(double NAT). It can be a second router of yours or a CGNAT of your ISP.",
        )

    return build(
        "no_evidence",
        "The first hops go from your private network straight to public addresses.",
    )
