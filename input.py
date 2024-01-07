import re
import os

from sql import *


def removeOldFiles(chat):
    outputFiles = [f"Output/{chat}/General.txt", f"Output/{chat}/Messages.txt", f"Output/{chat}/Words.txt", f"Output/{chat}/Emojis.txt"]
    for file in outputFiles:
        if os.path.exists(file):
            os.remove(file)


def addToDatabase(chat, data, first):
    removeOldFiles(chat)

    database = connect(chat)
    if first:
        createTable(database)
    if not first:
        lastMessage = selectLastMessage(database)
        lineFound = False
        lastLine = ""
    for line in data.split('\n'):
        reg = re.compile("([0-9]+)/([0-9]+)/([0-9]+), ([0-9]+):([0-9]+)\u202f(.{2}) - (.[^:]+): (.+)").match(line)
        if not first:
            if not lineFound:
                if reg and all(lastMessage[i] == reg.group(i) for i in range(1, 9)):
                    lineFound = True
                    continue
                elif not reg and re.compile("([0-9]+)/([0-9]+)/([0-9]+), (.+) - (.+)").match(line):
                    # Skip lines like this:
                    # 10/30/22, 9:08 AM - Person1 added Person2
                    # 12/15/22, 5:46 PM - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.
                    continue
                elif not reg:
                    # When a message has more lines
                    lastLine += '\n' + line.strip()
                    reg = re.compile("([0-9]+)/([0-9]+)/([0-9]+), ([0-9]+):([0-9]+)\u202f(.{2}) - (.[^:]+): (.+)").match(lastLine)
                    if reg and all(lastMessage[i] == reg.group(i) for i in range(1, 9)):
                        lineFound = True
                    continue
                elif reg:
                    lastLine = line
                    continue

        if reg:
            if reg.group(6) == "This message was deleted":
                continue
            insertMessage(database, *[reg.group(i) for i in range(1, 9)])
        elif re.compile("([0-9]+)/([0-9]+)/([0-9]+), (.+) - (.+)").match(line):
            # Skip lines like this:
            # 10/30/22, 9:08 AM - Person1 added Person2
            # 12/15/22, 5:46 PM - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.
            continue
        elif line != "":
            # When a message has more lines
            updateLastMessage(database, selectLastMessageText(database)[0] + '\n' + line.strip())
            continue
    disconnect(database)
