from modules.ping_test import ping_host
from modules.dns_lookup import dns_lookup
from modules.port_check import check_port
from modules.ip_info import get_local_ip, get_public_ip

from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

while True:

    # Header
    print(Fore.CYAN + Style.BRIGHT)
    print("=" * 35)
    print("   NETWORK DIAGNOSTIC TOOL")
    print("=" * 35)

    # Menu
    print(Fore.GREEN + "\n1 - Ping Test")
    print("2 - DNS Lookup")
    print("3 - Port Check")
    print("4 - Show Local IP")
    print("5 - Show Public IP")
    print(Fore.RED + "6 - Exit")

    # User choice
    choice = input(Fore.YELLOW + "\nSelect an option: ")

    # Ping Test
    if choice == "1":

        host = input(
            Fore.YELLOW + "\nEnter the IP address or domain: "
        )

        print(Fore.CYAN + "\nRunning Ping Test...\n")

        result = ping_host(host)

        print(Fore.WHITE + result)

    # DNS Lookup
    elif choice == "2":

        domain = input(
            Fore.YELLOW + "\nEnter the domain name: "
        )

        print(Fore.CYAN + "\nRunning DNS Lookup...\n")

        result = dns_lookup(domain)

        print(Fore.WHITE + result)

    # Port Check
    elif choice == "3":

        host = input(
            Fore.YELLOW + "\nEnter the host: "
        )

        try:

            port = int(
                input(
                    Fore.YELLOW + "Enter the port number: "
                )
            )

            print(Fore.CYAN + "\nChecking port status...\n")

            result = check_port(host, port)

            if "OPEN" in result.upper():
                print(Fore.GREEN + result)

            elif "CLOSED" in result.upper():
                print(Fore.RED + result)

            else:
                print(Fore.WHITE + result)

        except ValueError:
            print(
                Fore.RED +
                "\nInvalid port. Please enter a valid number."
            )

    # Local IP
    elif choice == "4":

        print(Fore.CYAN + "\nGetting local IP information...\n")

        result = get_local_ip()

        print(Fore.WHITE + result)

    # Public IP
    elif choice == "5":

        print(Fore.CYAN + "\nGetting public IP information...\n")

        result = get_public_ip()

        print(Fore.WHITE + result)

    # Exit
    elif choice == "6":

        print(
            Fore.YELLOW +
            "\nClosing Network Diagnostic Tool...\n"
        )

        break

    # Invalid Option
    else:

        print(
            Fore.RED +
            "\nInvalid option. Please try again.\n"
        )

    input(
        Fore.MAGENTA +
        "\nPress ENTER to return to the menu..."
    )