import emoji
from emoji import demojize
import datetime
import os

from sql import *
from output import writeData


def dataProcessing(chat):
    outputFiles = [f"Output/{chat}/General.txt", f"Output/{chat}/Messages.txt", f"Output/{chat}/Words.txt", f"Output/{chat}/Emojis.txt"]
    if all(os.path.exists(file) for file in outputFiles):
        return

    messagesNum, wordsNum, lettersNum, mediaNum, emojisNum = 0, 0, 0, 0, 0
    perUser, days, months, years, words, emojis = {}, {}, {}, {}, {}, {}
    dayOfTheWeek, hourOfTheDay = [0] * 7, [0] * 24
    firstMessage, lastMessage = {}, {}
    dates, maxWith, maxWithout = [], 0, 0

    database = connect(chat)
    for values in selectAllMessages(database):
        mes = {}
        keys = ["id", "month", "day", "year", "hour", "minute", "AM/PM", "person", "message"]
        for i in range(len(keys)):
            mes[keys[i]] = values[i]
        mes["year"] = "20" + mes["year"]

        messagesNum += 1
        messageSplit = mes["message"].split()
        if mes["message"] != "<Media omitted>":
            wordsNum += len(messageSplit)
            for word in messageSplit:
                if word.lower() not in words:
                    words[word.lower()] = 1
                else:
                    words[word.lower()] += 1

            lettersNum += sum(len(x) for x in messageSplit)

            emojiList = [demojize(x["emoji"]) for x in emoji.emoji_list(mes["message"])]
            if len(emojiList) > 0:
                emojisNum += len(emojiList)
                for e in emojiList:
                    if e not in emojis:
                        emojis[e] = 1
                    else:
                        emojis[e] += 1
        else:
            mediaNum += 1

        string = mes['year']
        if string not in years:
            years[string] = 1
        else:
            years[string] += 1

        string = f"{int(mes['month']):02d}/{mes['year']}"
        if string not in months:
            months[string] = 1
        else:
            months[string] += 1

        string = f"{int(mes['day']):02d}/{int(mes['month']):02d}/{mes['year']}"
        if string not in days:
            days[string] = 1
        else:
            days[string] += 1

        if mes["person"] not in perUser:
            # messagesNum, wordsNum, lettersNum, mediaNum, emojisNum, emojis, words
            perUser[mes["person"]] = [0, 0, 0, 0, 0, {}, {}]

        perUserPerson = perUser[mes["person"]]
        perUserPerson[0] += 1
        if mes["message"] != "<Media omitted>":
            perUserPerson[1] += len(messageSplit)
            for word in messageSplit:
                if word.lower() not in perUserPerson[6]:
                    perUserPerson[6][word.lower()] = 1
                else:
                    perUserPerson[6][word.lower()] += 1
            perUserPerson[2] += sum(len(x) for x in messageSplit)

            emojiList = [demojize(x["emoji"]) for x in emoji.emoji_list(mes["message"])]
            if len(emojiList) > 0:
                perUserPerson[4] += len(emojiList)
                for e in emojiList:
                    if e not in perUserPerson[5]:
                        perUserPerson[5][e] = 1
                    else:
                        perUserPerson[5][e] += 1
        else:
            perUserPerson[3] += 1

        date = datetime.datetime(int(mes["year"]), int(mes["month"]), int(mes["day"]))
        dayOfTheWeek[(int(date.strftime("%w")) - 1) % 7] += 1
        if mes["AM/PM"] == "AM":
            hourOfTheDay[int(mes["hour"]) % 12] += 1
        else:
            hourOfTheDay[int(mes["hour"]) % 12 + 12] += 1

        if mes["person"] not in firstMessage:
            firstMessage[mes["person"]] = f"{mes['day']}/{mes['month']}/{mes['year']} {mes['hour']}:{mes['minute']}{mes['AM/PM']}"
            lastMessage[mes["person"]] = f"{mes['day']}/{mes['month']}/{mes['year']} {mes['hour']}:{mes['minute']}{mes['AM/PM']}"
        else:
            lastMessage[mes["person"]] = f"{mes['day']}/{mes['month']}/{mes['year']} {mes['hour']}:{mes['minute']}{mes['AM/PM']}"

        if date not in dates:
            dates.append(date)

    cur = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days - 1 > maxWithout:
            maxWithout = (dates[i] - dates[i - 1]).days - 1
        if (dates[i] - dates[i - 1]).days == 1:
            cur += 1
        else:
            if cur > maxWith:
                maxWith = cur
            cur = 1
    if cur > maxWith:
        maxWith = cur

    disconnect(database)

    writeData(chat, messagesNum, wordsNum, lettersNum, mediaNum, emojisNum, perUser, days, months, years, words, emojis, dayOfTheWeek, hourOfTheDay, firstMessage, lastMessage, maxWith, maxWithout)
