import re
import os

from sql import *

def removeOldFiles():
    outputFiles = ["Stats/General.txt", "Stats/Messages.txt", "Stats/Words.txt", "Stats/Emojis.txt"]
    for file in outputFiles:
        if os.path.exists(file):
            os.remove(file)


def addToDatabase(chat, data, first):
    database = connect(chat)
    if first:
        createTable(database)
        firstLine = True
    if not first:
        lastMessage = selectLastMessage(database)
        lineFound = False
        lastLine = ""
    for line in data.split('\n'):
        if first:
            if firstLine:
                firstLine = False
                continue
        reg = re.compile("([0-9]+)/([0-9]+)/([0-9]+), ([0-9]+):([0-9]+)\u202f(.{2}) - (.[^:]+): (.+)").match(line)
        if not first:
            if not lineFound:
                if reg and all(lastMessage[i] == reg.group(i) for i in range(1, 9)):
                    lineFound = True
                    continue
                elif not reg and re.compile("([0-9]+)/([0-9]+)/([0-9]+), (.+) - (.+)").match(line):
                    continue
                elif not reg:
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
            continue
        elif line != "":
            updateLastMessage(database, selectLastMessageText(database)[0] + '\n' + line.strip())
            continue
    disconnect(database)


