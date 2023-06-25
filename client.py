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
    print("Starting the chat, type 'quit' or press Ctrl-D to exit.")

    while True:
        try:
            user_message = input(Fore.GREEN + "User: " + Style.RESET_ALL)
        except EOFError:
            break

        if user_message.lower() == "quit":
            break

        response = send_message(user_message)
        print(Fore.BLUE + "Zeus: " + Style.RESET_ALL + response.get("response", ""))


if __name__ == "__main__":
    chat()
