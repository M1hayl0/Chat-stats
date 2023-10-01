import re
import os


def removeOldFiles(chat):
    outputFiles = ["Stats/General.txt", "Stats/Messages.txt", "Stats/Words.txt", "Stats/Emojis.txt"]
    for file in outputFiles:
        if os.path.exists(file):
            os.remove(file)

    if os.path.exists(f"Input/{chat}/{chat}.txt"):
        os.remove(f"Input/{chat}/{chat}.txt")


def mergeNewFiles(chat):
    inputFiles = []
    for filename in os.listdir(f"Input/{chat}"):
        inputFiles.append(f"Input/{chat}/{filename}")

    id = 1
    firstFile = True
    firstLine = True
    with open(f"Input/{chat}/{chat}.txt", "a", encoding="utf8") as outputFile:
        for file in inputFiles:
            lineFound = True if firstFile else False

            with open(file, encoding="utf8") as inputFile:
                for line in inputFile:
                    if firstLine:
                        firstLine = False
                        continue

                    if not lineFound and f"id{id - 1}, " + line == lastLine:
                        lineFound = True
                        continue
                    elif lineFound:
                        if re.compile("([0-9]+)/([0-9]+)/([0-9]+), ([0-9]+):([0-9]+)\u202f(.{2}) - (.[^:]+): (.+)").match(line):
                            line = f"id{id}, " + line
                            id += 1
                        elif re.compile("([0-9]+)/([0-9]+)/([0-9]+), (.+) - (.+)").match(line):
                            continue
                        outputFile.write(line)
                        lastLine = line

            firstFile = False


def readData(chat):
    keys = ["id", "month", "day", "year", "hour", "minute", "AM/PM", "person", "message"]
    data = []

    with open(f"Input/{chat}/{chat}.txt", encoding="utf8") as inputFile:
        for line in inputFile:
            reg = re.compile("id([0-9]+), ([0-9]+)/([0-9]+)/([0-9]+), ([0-9]+):([0-9]+)\u202f(.{2}) - (.[^:]+): (.+)").match(line)
            if not reg:
                data[-1]["message"] += '\n' + line.strip()
                continue

            if reg.group(6) == "This message was deleted":
                continue

            dic = {}
            for i in range(len(keys)):
                dic[keys[i]] = reg.group(i + 1)
            dic["year"] = "20" + dic["year"]
            data.append(dic)

    return data
