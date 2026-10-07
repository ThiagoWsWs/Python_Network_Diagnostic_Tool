from colorama import Fore, Style, init

from modules.dns_lookup import dns_lookup
from modules.ip_info import get_local_ip, get_public_ip
from modules.ping_test import ping_host
from modules.port_check import check_port

# Initialize Colorama
init(autoreset=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ask(prompt):
    """Ask the user for input using the prompt color."""
    return input(Fore.YELLOW + prompt).strip()


def print_error(message):
    print(Fore.RED + f"\n{message}")


def show_menu():
    print(Fore.CYAN + Style.BRIGHT + "\n" + "=" * 35)
    print(Fore.CYAN + Style.BRIGHT + "   NETWORK DIAGNOSTIC TOOL")
    print(Fore.CYAN + Style.BRIGHT + "=" * 35 + "\n")

    for key, (label, action) in MENU_OPTIONS.items():
        color = Fore.RED if action is None else Fore.GREEN
        print(color + f"{key} - {label}")


# ---------------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------------

def ping_menu():
    host = ask("\nEnter the IP address or domain: ")

    print(Fore.CYAN + "\nRunning Ping Test...\n")

    result = ping_host(host)

    if result["output"]:
        print(Fore.WHITE + result["output"])

    if result["success"]:
        print(Fore.GREEN + f"\nHost is reachable (average: {result['average_ms']} ms)")
    else:
        print_error(result["error"])


def dns_menu():
    domain = ask("\nEnter the domain name: ")

    print(Fore.CYAN + "\nRunning DNS Lookup...\n")

    result = dns_lookup(domain)

    if not result["success"]:
        print_error(result["error"])
        return

    ipv4 = ", ".join(result["ipv4"]) or "Not found"
    ipv6 = ", ".join(result["ipv6"]) or "Not found"
    hostname = result["hostname"] or "Reverse DNS not available"

    print(Fore.WHITE + f"""=== DNS LOOKUP RESULT ===

Domain: {result['domain']}
IPv4 Address: {ipv4}
IPv6 Address: {ipv6}
Hostname: {hostname}
""")


def port_menu():
    host = ask("\nEnter the host: ")

    try:
        port = int(ask("Enter the port number: "))
    except ValueError:
        print_error("Invalid port. Please enter a valid number.")
        return

    print(Fore.CYAN + "\nChecking port status...\n")

    result = check_port(host, port)

    if not result["success"]:
        print_error(result["error"])
        return

    service = f" ({result['service']})" if result["service"] else ""

    if result["is_open"]:
        print(Fore.GREEN + f"Port {result['port']}{service} is OPEN on {result['host']}")
    else:
        print(Fore.RED + f"Port {result['port']}{service} is CLOSED or filtered on {result['host']}")


def local_ip_menu():
    print(Fore.CYAN + "\nGetting local IP information...\n")

    result = get_local_ip()

    if result["success"]:
        print(Fore.WHITE + f"=== LOCAL IP INFORMATION ===\n\nLocal IP: {result['ip']}\n")
    else:
        print_error(result["error"])


def public_ip_menu():
    print(Fore.CYAN + "\nGetting public IP information...\n")

    result = get_public_ip()

    if result["success"]:
        print(Fore.WHITE + f"=== PUBLIC IP INFORMATION ===\n\nPublic IP: {result['ip']}\n")
    else:
        print_error(result["error"])


# ---------------------------------------------------------------------------
# Menu definition: key -> (label, function). A function of None means "Exit".
# To add a new feature, create its function above and add one line here.
# ---------------------------------------------------------------------------

MENU_OPTIONS = {
    "1": ("Ping Test", ping_menu),
    "2": ("DNS Lookup", dns_menu),
    "3": ("Port Check", port_menu),
    "4": ("Show Local IP", local_ip_menu),
    "5": ("Show Public IP", public_ip_menu),
    "6": ("Exit", None),
}


def main():
    while True:
        show_menu()

        choice = ask("\nSelect an option: ")

        if choice not in MENU_OPTIONS:
            print(Fore.RED + "\nInvalid option. Please try again.\n")
        else:
            _, action = MENU_OPTIONS[choice]

            if action is None:
                print(Fore.YELLOW + "\nClosing Network Diagnostic Tool...\n")
                break

            action()

        input(Fore.MAGENTA + "\nPress ENTER to return to the menu...")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(Fore.YELLOW + "\n\nInterrupted by user. Goodbye!\n")
