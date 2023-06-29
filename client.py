import os
import sys

if os.name == "nt":  # Windows
    import pyreadline as readline
elif sys.platform == "darwin":  # macOS
    import gnureadline as readline
else:
    import readline  # Linux

import requests
from colorama import Fore, Style
import json
import signal
import sys


def signal_handler(sig, frame):
    print(Fore.RED + "\nExiting chat..." + Style.RESET_ALL)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# PANTHEON_SERVER_IP is localhost unless set as an environment variable
PANTHEON_SERVER_IP = os.environ.get("PANTHEON_SERVER_IP", "localhost")
PANTHEON_SERVER_PORT = os.environ.get("PANTHEON_SERVER_PORT", "5000")


def send_message(message):
    # send message to flask server, connect to localhost:5000 by default unless PANTHEON_SERVER_IP is set
    response = requests.post(
        f"http://{PANTHEON_SERVER_IP}:{PANTHEON_SERVER_PORT}/generate_message",
        data=json.dumps({"message": message}),
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
            user_message = input(Fore.YELLOW + "User: " + Style.RESET_ALL)
        except EOFError:
            break

        if user_message.startswith("/"):
            handle_command(user_message)
            continue

        response = send_message(user_message)
        print(Fore.BLUE + "Zeus: " + Style.RESET_ALL + response.get("response", ""))


def prompts():
    response = requests.get(f"http://{PANTHEON_SERVER_IP}:{PANTHEON_SERVER_PORT}/prompts")
    return response.json()


def help():
    print(Fore.GREEN + "/help" + Style.RESET_ALL + " - show this help message")
    print(Fore.GREEN + "/prompts" + Style.RESET_ALL + " - show list of prompts")
    print(Fore.GREEN + "/exit (Ctrl-D)" + Style.RESET_ALL + " - exit the chat")
    print(Fore.GREEN + "You can use arrow keys to navigate the chat history\n" + Style.RESET_ALL)


def handle_command(command):
    if command == "/prompts":
        print("Available prompts:")
        for prompt in prompts()["prompts"]:
            print(f" - {prompt}")
    elif command == "/help":
        help()
    elif command == "/exit":
        sys.exit(0)
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    chat()
