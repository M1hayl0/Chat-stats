import re
import os
import datetime

from sql import *


def removeOldFiles(chat):
    outputFiles = [f"Output/{chat}/General.txt", f"Output/{chat}/Messages.txt", f"Output/{chat}/Words.txt", f"Output/{chat}/Emojis.txt"]
    for file in outputFiles:
        if os.path.exists(file):
            os.remove(file)


def addToDatabaseWa(chat, data, first, createTableBool):
    removeOldFiles(chat)

    database = connect(chat)
    if createTableBool:
        createTable(database)
    if not first:
        lastMessage = selectLastMessage(database, "wa")
        lastLine = ""
        if not lastMessage:
            first = True
        else:
            lineFound = False
    for line in data.split('\n'):
        reg = re.compile("([0-9]+)/([0-9]+)/([0-9]+), ([0-9]+):([0-9]+)\u202f(.{2}) - (.[^:]+): (.+)").match(line)
        if not first and not lineFound:
            if reg and all(lastMessage[i] == reg.group(i) for i in range(1, 9)) and lastMessage[-1] == "wa":
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
                if reg and all(lastMessage[i] == reg.group(i) for i in range(1, 9)) and lastMessage[-1] == "wa":
                    lineFound = True
                continue
            elif reg:
                lastLine = line
                continue

        if reg:
            if reg.group(6) == "This message was deleted":
                continue
            insertMessage(database, *[reg.group(i) for i in range(1, 9)], "wa")
        elif re.compile("([0-9]+)/([0-9]+)/([0-9]+), (.+) - (.+)").match(line):
            # Skip lines like this:
            # 10/30/22, 9:08 AM - Person1 added Person2
            # 12/15/22, 5:46 PM - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.
            continue
        elif line != "":
            # When a message has more lines
            updateLastMessage(database, selectLastMessageText(database, "wa")[0] + '\n' + line.strip(), "wa")
            continue
    disconnect(database)

    if not first and not lineFound:
        addToDatabaseInsta(chat, data, True, False)


def addToDatabaseInsta(chat, data, first, createTableBool):
    removeOldFiles(chat)
    database = connect(chat)

    if createTableBool:
        createTable(database)
    if not first:
        lastMessage = selectLastMessage(database, "insta")
        if not lastMessage:
            first = True
        else:
            lineFound = False
    for mes in data["messages"]:
        # when a person likes your message, a message is added for them saying that your message has been liked, skip those messages
        # the text of this message is in my language because that's how I found it in some chat, it probably can be in any other language but there is no smart way I can solve it because the data for it is same as the data for a regular message
        # if the person you are chatting with has much more messages than you, try changing this string
        if "content" in mes and mes["content"] == "\u00d0\u00a1\u00d0\u00b2\u00d0\u00b8\u00d1\u0092\u00d0\u00b0 \u00d0\u00bc\u00d1\u0083/\u00d1\u0098\u00d0\u00be\u00d1\u0098 \u00d1\u0081\u00d0\u00b5 \u00d0\u00bf\u00d0\u00be\u00d1\u0080\u00d1\u0083\u00d0\u00ba\u00d0\u00b0":
            continue

        timestamp_s = mes["timestamp_ms"] / 1000
        utcDt = datetime.datetime.fromtimestamp(timestamp_s, datetime.timezone.utc)
        utcPlus2 = datetime.timezone(datetime.timedelta(hours=2))
        localizedDt = utcDt.astimezone(utcPlus2)

        month = str(localizedDt.month)
        day = str(localizedDt.day)
        year = str(localizedDt.year % 100).zfill(2)
        hour = localizedDt.hour if localizedDt.hour <= 12 else localizedDt.hour - 12  # correct time only for UTC+2 timezone
        if hour == 0:
            hour = 12
        hour = str(hour)
        minute = str(localizedDt.minute).zfill(2)
        AMPM = "AM" if localizedDt.hour < 12 else "PM"

        person = mes["sender_name"].encode('latin1').decode('utf-8')
        if "content" in mes:
            message = mes["content"]
            message = message.encode('latin1').decode('utf-8')
        elif "photos" in mes:
            message = "<Media omitted>"

        data2 = [month, day, year, hour, minute, AMPM, person, message, "insta"]
        if not first and not lineFound:
            if all(lastMessage[i] == data2[i - 1] for i in range(1, 10)):
                lineFound = True
                continue
        else:
            insertMessage(database, *data2)

    disconnect(database)

    if not first and not lineFound:
        addToDatabaseInsta(chat, data, True, False)
