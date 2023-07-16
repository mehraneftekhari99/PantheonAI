import os
import sys
import json
import signal
import random
import textwrap
import readline
import requests
from colorama import Fore, Style


def signal_handler(sig, frame):
    print(Fore.RED + "\nExiting chat..." + Style.RESET_ALL)
    sys.exit(0)

# client should not exit on exceptions, but print them instead and prompt for new input
sys.excepthook = lambda *args: print(Fore.RED + "Error:", *args, Style.RESET_ALL)


signal.signal(signal.SIGINT, signal_handler)

# PANTHEON_SERVER_IP is localhost unless set as an environment variable
PANTHEON_SERVER_IP = os.environ.get("PANTHEON_SERVER_IP", "localhost")
PANTHEON_SERVER_PORT = os.environ.get("PANTHEON_SERVER_PORT", "5000")
# Set a random username from cities list unless set as an environment variable
CITIES = [line.strip("\n") for line in open("resources/cities.txt")]
USERNAME = os.environ.get("USERNAME", CITIES[random.randint(0, len(CITIES) - 1)])


def send_message(message):
    response = requests.post(
        f"http://{PANTHEON_SERVER_IP}:{PANTHEON_SERVER_PORT}/generate_message_with_history",
        data=json.dumps({"message": message, "user": USERNAME}),
        headers={"Content-Type": "application/json"},
    )

    return response.json()


def chat():
    print(
        Fore.LIGHTCYAN_EX
        + "Starting the chat, type '/help' to show list of commands. Press Ctrl-D to exit."
        + Style.RESET_ALL
    )

    while True:
        try:
            user_message = input(Fore.YELLOW + f"{USERNAME}: " + Style.RESET_ALL)
        except EOFError:
            break

        if user_message.startswith("/"):
            handle_command(user_message)
            continue

        response = send_message(user_message)
        print(Fore.BLUE + "Pantheon: " + Style.RESET_ALL + response.get("response", ""))


def prompts():
    response = requests.get(f"http://{PANTHEON_SERVER_IP}:{PANTHEON_SERVER_PORT}/prompts")
    return response.json()

def memory():
    response = requests.get(f"http://{PANTHEON_SERVER_IP}:{PANTHEON_SERVER_PORT}/memory/{USERNAME}")
    return response.json()


def help():
    help_text = f"""
        {Style.BRIGHT}Pantheon Client{Style.RESET_ALL} - List of commands:
        {Fore.GREEN}/help{Style.RESET_ALL} - show this help message
        {Fore.GREEN}/prompts{Style.RESET_ALL} - show list of prompts
        {Fore.GREEN}/summary{Style.RESET_ALL} - show summary of the conversation
        {Fore.GREEN}/setuser <user>{Style.RESET_ALL} - set the user name to <user>, if <user> is not provided, a random name is set
        {Fore.GREEN}/exit (Ctrl-D){Style.RESET_ALL} - exit the chat
        {Fore.GREEN}You can use arrow keys to navigate the chat history.{Style.RESET_ALL}"""
    print(textwrap.dedent(help_text))


def setuser(user=None):
    global USERNAME
    if user is None:
        user = CITIES[random.randint(0, len(CITIES) - 1)]
    USERNAME = user
    print(f"Username set to {USERNAME}")


def handle_command(command):
    if command == "/prompts":
        print("\n".join([f" - {prompt}" for prompt in prompts()["prompts"]]))
    elif command == "/memory":
        print(memory())
    elif command == "/summary":
        print(memory()["memory"]["summary"]["content"])
    elif command.startswith("/setuser"):
        setuser(command.split(" ")[1] if len(command.split(" ")) > 1 else None)
    elif command == "/help":
        help()
    elif command == "/exit":
        sys.exit(0)
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    chat()
