from modules.ping_test import ping_host
from modules.dns_lookup import dns_lookup
from modules.port_check import check_port

from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

while True:

    # Header
    print(Fore.CYAN + Style.BRIGHT + "\n=== NETWORK DIAGNOSTIC TOOL ===\n")

    # Menu options
    print(Fore.GREEN + "1 - Ping Test")
    print(Fore.GREEN + "2 - DNS Lookup")
    print(Fore.GREEN + "3 - Port Check")
    print(Fore.RED + "4 - Exit")

    # User choice
    choice = input(Fore.YELLOW + "\nSelect an option: ")

    # Ping Test
    if choice == "1":

        host = input(Fore.YELLOW + "\nEnter the IP or domain: ")

        print(Fore.CYAN + "\nRunning ping test...\n")

        result = ping_host(host)

        print(Fore.WHITE + result)

    # DNS Lookup
    elif choice == "2":

        domain = input(Fore.YELLOW + "\nEnter the domain: ")

        print(Fore.CYAN + "\nRunning DNS lookup...\n")

        result = dns_lookup(domain)

        print(Fore.WHITE + result)

    # Port Check
    elif choice == "3":

        host = input(Fore.YELLOW + "\nEnter the host: ")

        try:

            port = int(input(Fore.YELLOW + "Enter the port: "))

            print(Fore.CYAN + "\nChecking port status...\n")

            result = check_port(host, port)

            # Green if open
            if "OPEN" in result:
                print(Fore.GREEN + result)

            # Red if closed
            elif "CLOSED" in result:
                print(Fore.RED + result)

            else:
                print(Fore.WHITE + result)

        except ValueError:
            print(Fore.RED + "\nInvalid port. Please enter a valid number.")

    # Exit
    elif choice == "4":

        print(Fore.YELLOW + "\nClosing Network Diagnostic Tool...\n")

        break

    # Invalid option
    else:
        print(Fore.RED + "\nInvalid option. Please try again.\n")