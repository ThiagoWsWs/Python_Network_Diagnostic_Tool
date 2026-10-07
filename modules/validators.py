import ipaddress
import re

# One hostname label: 1-63 chars, letters/digits/hyphens, no hyphen at start or end
_LABEL = r"(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
_HOSTNAME_PATTERN = re.compile(rf"^(?=.{{1,253}}$){_LABEL}(\.{_LABEL})*$")


def is_valid_ip(value):
    """Return True if value is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(str(value).strip())
        return True
    except ValueError:
        return False


def is_valid_host(value):
    """Return True if value is a valid IP address or hostname/domain.

    Also blocks values starting with '-', which could be interpreted
    as command-line options when passed to external commands like ping.
    """
    if not isinstance(value, str):
        return False

    value = value.strip()

    if not value:
        return False

    return is_valid_ip(value) or bool(_HOSTNAME_PATTERN.match(value))


def is_valid_port(port):
    """Return True if port is an integer between 1 and 65535."""
    return isinstance(port, int) and not isinstance(port, bool) and 1 <= port <= 65535
