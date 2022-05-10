#! /usr/bin/python3
# Isaac Ganoung
import sys

def process_command(input_line):
    """Process a command, and discard extra output. Raises RuntimeError if command is unknown.
    Possible commands:
    p
    d <line number>
    r
    g <gopher url>
    """
    command = input_line.split(' ')
    # If statement block is possible here because of limited number of commands
    if command[0][0] == 'p':
        return 'print'
    elif command[0][0] == 'd' and len(command) >= 2 and command[1].isnumeric():
        return 'download',int(command[1])
    elif command[0][0] == 'd':
        raise RuntimeError("Unable to download ''")
    elif command[0][0] == 'r':
        return 'reload'
    elif command[0][0] == 'g':
        if len(command) < 2:
            raise RuntimeError("Unable to navigate to ''")
        return 'goto_url',command[1]
    elif command[0] == '\f':
        return 'clear'
    else:
        raise RuntimeError(f"Unknown command \"{command[0]}\"")


def get_input(url):
    """Display the prompt, including the current directory URL. Returns input."""
    if url != "":
        return process_command(input(f"{url} ゴーファー> "))
    return process_command(input("ゴーファー> "))
