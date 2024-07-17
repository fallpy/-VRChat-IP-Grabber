import os
import sys
import subprocess
import socket
import concurrent.futures
import random
import time
import requests
from colorama import init, Fore, Style
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

# Initialize colorama for colored output
init()

# Define colors
ORANGE = Fore.LIGHTYELLOW_EX
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Style.RESET_ALL

# Function to clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the F4 HUB ASCII art
def print_ascii_art():
    ascii_art = """
                                 ██████▒██░ ██    ██░ ██  █    ██  ▄▄▄▄   
                                ▓██   ▒▓██░ ██▒  ▓██░ ██▒ ██  ▓██▒▓█████▄ 
                                ▒████  ░░▀▀▀██░  ▒██▀▀██░▓██  ▒██░▒██▒ ▄██
                                ░▓█▒     ░░░██   ░▓█ ░██ ▓▓█  ░██░▒██░█▀  
                                ░▒█░   ░  ▒░██   ░▓█▒░██▓▒▒█████▓ ░▓█  ▀█▓
                                 ▒ ░    ▒ ░░▒░▒    ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░▒▓███▀▒
                                 ░      ▒ ░▒░ ░    ▒ ░▒░ ░░░▒░ ░ ░ ▒░▒   ░ 
                                 ░ ░    ░  ░░ ░    ░  ░░ ░ ░░░ ░ ░  ░    ░ 
                                        ░  ░  ░    ░  ░  ░   ░      ░      
                                                                         ░ 
    """
    print(f"{ORANGE}{ascii_art}{RESET}")

# Function to display the main menu centered
def display_menu():
    options = [
        "[=] 1 Convert YouTube URL to CDNApp URL            [=] SOON..",
        "[=] 2 IP Information Lookup                        [=] SOON..",
        "[=] 3 Create Dox                                   [=] SOON..",
        "[=] 4 Get User Info and Notify                     [=] SOON..",
        "[=] 5 PHONE NUMBER TRACKER                         [=] SOON..",
        "[=] 6 UNDEFINED ⚠️ DO NOT USE ⚠️                  [=] SOON..",
        "[=] SOON..                                         [=] SOON..",
        "[=] SOON..                                         [=] SOON..",
        "[=] SOON..                                         [=] SOON..",
        "[=] SOON..                                         [=] SOON..",
        "[=] 00 Exit                                         [=] SOON..",
    ]
    clear_screen()
    print_ascii_art()

    # Calculate center alignment for the title
    title = "F4 HUB"
    title_margin = (80 - len(title)) // 2  # Assuming terminal width is 80 characters
    print(f"{ORANGE}{' ' * title_margin}{title}{' ' * title_margin}{RESET}")

    print("Please select an option:")
    for option in options:
        # Calculate center alignment for each option
        print(f"{GREEN}{option}{RESET}")
    print(f"{ORANGE}==========================================================================================================================={RESET}")

    return options

# Function to get user choice from the main menu
def get_user_choice():
    while True:
        try:
            choice = int(input(f"{ORANGE}Enter your choice (0-5): {RESET}"))
            if 0 <= choice <= 5 or ("hi"):
                return choice
            else:
                print(f"{ORANGE}Invalid choice. Please enter a number between 0 and 5.{RESET}")
        except ValueError:
            print(f"{ORANGE}Invalid input. Please enter a number.{RESET}")

# Function to convert YouTube URL to CDNApp URL
def youtube_to_cdnapp():
    clear_screen()
    while True:
        youtube_url = input(f"{ORANGE}Enter a YouTube URL (or type '/exit' to quit): {RESET}")

        if youtube_url.lower() == '/exit':
            print("Exiting YouTube to CDNApp conversion.")
            time.sleep(1)
            return
        elif youtube_url.lower() == '/help':
            display_menu()
            continue

        video_id = extract_video_id(youtube_url)

        if video_id:
            cdnapp_url = f"https://cdnapp.de/watch?v={video_id}"
            print(f"{GREEN}CDNApp URL: {cdnapp_url}{RESET}")
        else:
            print(f"{ORANGE}Invalid YouTube URL format. Please provide a URL with 'watch?v='.{RESET}")
        input("\nPress Enter to continue...")

# Function to extract video ID from YouTube URL
def extract_video_id(youtube_url):
    if 'watch?v=' in youtube_url:
        video_id_start_index = youtube_url.index('watch?v=') + len('watch?v=')
        video_id = youtube_url[video_id_start_index:]
        if '&' in video_id:
            video_id = video_id[:video_id.index('&')]
        return video_id
    else:
        return None

# Function for IP information lookup
def ip_information_lookup():
    try:
        clear_screen()
        ip = input(f"{ORANGE}Enter an IP address to lookup: {RESET}")

        # Function to ping the IP address
        def ping_ip(ip):
            try:
                if sys.platform.startswith("win"):
                    result = subprocess.run(['ping', '-n', '1', ip], capture_output=True, text=True, timeout=1)
                elif sys.platform.startswith("linux"):
                    result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, text=True, timeout=1)
                if result.returncode == 0:
                    ping_status = f"{GREEN}Succeed{RESET}"
                else:
                    ping_status = f"{RED}Fail{RESET}"
            except:
                ping_status = f"{RED}Fail{RESET}"
            print(f"{ORANGE}Ping Status   : {ping_status}")

        # Function to check open ports on the IP address
        open_ports = []
        def check_open_ports(ip):
            def scan_port(ip, port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass

            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = {executor.submit(scan_port, ip, port): port for port in range(1, 1000 + 1)}
            concurrent.futures.wait(results)

            print(f"{ORANGE}Open Ports    : {open_ports}")

        # Function to perform DNS lookup
        def dns_lookup(ip):
            try:
                dns, _, _ = socket.gethostbyaddr(ip)
            except:
                dns = "None"
            print(f"{ORANGE}DNS           : {dns}")

        # Function to fetch IP information from APIs
        def fetch_ip_info(ip):
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}")
                if response.status_code == 200:
                    api_data = response.json()
                    print(f"{ORANGE}IP Information:")
                    print(f"   Status      : {api_data['status']}")
                    print(f"   Country     : {api_data['country']} ({api_data['countryCode']})")
                    print(f"   Region      : {api_data['regionName']} ({api_data['region']})")
                    print(f"   City        : {api_data['city']}")
                    print(f"   Zip Code    : {api_data['zip']}")
                    print(f"   ISP         : {api_data['isp']}")
                    print(f"   AS          : {api_data['as']}")
                    print(f"   Google Maps : https://www.google.com/maps/search/?api=1&query={api_data['lat']},{api_data['lon']}")
                else:
                    print(f"{RED}Failed to fetch IP information from API.{RESET}")
            except Exception as e:
                print(f"{RED}Error fetching IP information: {e}{RESET}")

        print(f"{ORANGE}Fetching information for IP: {ip}{RESET}")
        ping_ip(ip)
        check_open_ports(ip)
        dns_lookup(ip)
        fetch_ip_info(ip)
        input("\nPress Enter to continue...")

    except Exception as e:
        print(f"{RED}Error in IP information lookup: {e}{RESET}")

# Function for creating dox
def create_dox():
    try:
        clear_screen()
        name = input(f"{ORANGE}Enter the name of the person for doxing: {RESET}")
        location = input(f"{ORANGE}Enter their location (city, state, country zip, code): {RESET}")
        ip_dox = input(f"{ORANGE}Enter their location (city, state): {RESET}")
        age = input(f"{ORANGE}Enter their age: {RESET}")
        phone = input(f"{ORANGE}Enter their phone number: {RESET}")
        social_media = input(f"{ORANGE}Enter their social media profiles: {RESET}")

        # Generate a random ID
        user_id = random.randint(100000, 999999)

        clear_screen()
        print(f"{ORANGE}Generated DOX Information:{RESET}")
        print(f"{ORANGE}ID: {user_id}{RESET}")
        print(f"{ORANGE}Name: {name}{RESET}")
        print(f"{ORANGE}Location: {location}{RESET}")
        print(f"{ORANGE}Age: {age}{RESET}")
        print(f"{ORANGE}Phone: {phone}{RESET}")
        print(f"{ORANGE}Social Media Profiles: {social_media}{RESET}")
        input("\nPress Enter to continue...")

    except Exception as e:
        print(f"{RED}Error creating dox: {e}{RESET}")

# Function for getting user info and notifying them via Discord webhook
def get_user_info_and_notify():
    try:
        clear_screen()
        webhook_url = input(f"{ORANGE}Enter the Discord webhook URL: {RESET}")
        name = input(f"{ORANGE}Enter the user's name: {RESET}")
        user_id = input(f"{ORANGE}Enter the user's ID: {RESET}")
        ip = input(f"{ORANGE}Enter the user's IP address: {RESET}")
        phone_number = input(f"{ORANGE}Enter the user's phone number: {RESET}")

        message = f"**User Information**\n\n**Name:** {name}\n**User ID:** {user_id}\n**IP Address:** {ip}\n**Phone Number:** {phone_number}"

        # Send the message to the Discord webhook
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code == 204:
            print(f"{GREEN}User information sent successfully to the Discord webhook.{RESET}")
        else:
            print(f"{RED}Failed to send user information to the Discord webhook. Status code: {response.status_code}{RESET}")

        input("\nPress Enter to continue...")

    except Exception as e:
        print(f"{RED}Error in getting user info and notifying: {e}{RESET}")


def number_info():
    try:
        phone_number = input(f"\nEnter Phone Number -> ")
        parsed_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            if phone_number.startswith("+"):
                country_code = "+" + phone_number[1:3]
            else:
                country_code = "None"
            operator = carrier.name_for_number(parsed_number, "en")
            type_number = "Mobile" if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else "Fixed"
            timezones = timezone.time_zones_for_number(parsed_number)
            timezone_info = timezones[0] if timezones else None
            country = phonenumbers.region_code_for_number(parsed_number)
            region = geocoder.description_for_number(parsed_number, "en")
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            status = "Valid"
        else:
            formatted_number = "None"
            region = "None"
            country = "None"
            operator = "None"
            type_number = "None"
            timezone_info = "None"
            country_code = "None"
            status = "Invalid"

        print(f"""
Phone        : {phone_number}
Formatted    : {formatted_number}
Status       : {status}
Country Code : {country_code}
Country      : {country}
Region       : {region}
Timezone     : {timezone_info}
Operator     : {operator}
Type Number  : {type_number}
""")
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"Error: {e}")
    

# Main loop
while True:
    options = display_menu()
    choice = get_user_choice()

    if choice == 1:
        youtube_to_cdnapp()
    elif choice == 2:
        ip_information_lookup()
    elif choice == 3:
        create_dox()
    elif choice == 4:
        get_user_info_and_notify()
    elif choice == 5:
        number_info()
    elif choice == 00:
        print("Exiting F4 HUB. Goodbye!")
        break
    else:
        print("Invalid choice. Please choose another option.")