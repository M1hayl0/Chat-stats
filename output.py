from emoji import emojize


def writeData(chat, messagesNum, wordsNum, lettersNum, mediaNum, emojisNum, perUser, days, months, years, words, emojis, dayOfTheWeek, hourOfTheDay, firstMessage, lastMessage, maxWith, maxWithout):
    with open("Stats/General.txt", "a", encoding="utf8") as outputFileGeneral:
        outputFileGeneral.write(f"Total messages: {messagesNum}\n")
        outputFileGeneral.write(f"Total words: {wordsNum}\n")
        outputFileGeneral.write(f"Total letters: {lettersNum}\n")
        outputFileGeneral.write(f"Total media files: {mediaNum}\n")
        outputFileGeneral.write(f"Total emojis: {emojisNum}\n\n")

        outputFileGeneral.write("Messages per user: \n")
        [outputFileGeneral.write(f"{key}: {value[0]}\n") for key, value in sorted(perUser.items(), key=lambda x: x[1][0], reverse=True)]
        outputFileGeneral.write("\n")

        outputFileGeneral.write("Words per user: \n")
        [outputFileGeneral.write(f"{key}: {value[1]}\n") for key, value in sorted(perUser.items(), key=lambda x: x[1][1], reverse=True)]
        outputFileGeneral.write("\n")

        outputFileGeneral.write("Letters per user: \n")
        [outputFileGeneral.write(f"{key}: {value[2]}\n") for key, value in sorted(perUser.items(), key=lambda x: x[1][2], reverse=True)]
        outputFileGeneral.write("\n")

        outputFileGeneral.write("Average of letters per message: \n")
        [outputFileGeneral.write(f"{key}: {round(value[2]/value[0])}\n") for key, value in sorted(perUser.items(), key=lambda x: x[1][2]/x[1][0], reverse=True)]
        outputFileGeneral.write("\n")

        outputFileGeneral.write("Media files per user: \n")
        [outputFileGeneral.write(f"{key}: {value[3]}\n") for key, value in sorted(perUser.items(), key=lambda x: x[1][3], reverse=True)]
        outputFileGeneral.write("\n")

        outputFileGeneral.write(f"Most consecutive days chatting: {maxWith}\n")
        outputFileGeneral.write(f"Most consecutive days without messages: {maxWithout}\n")
        outputFileGeneral.write("\n")

        outputFileGeneral.write("First message: \n")
        for key, value in firstMessage.items():
            outputFileGeneral.write(f"{key}: {value}\n")
        outputFileGeneral.write("\n")

        outputFileGeneral.write("Last message: \n")
        for key, value in lastMessage.items():
            outputFileGeneral.write(f"{key}: {value}\n")
        outputFileGeneral.write("\n")

    with open("Stats/Messages.txt", "a", encoding="utf8") as outputFileMessages:
        outputFileMessages.write("Messages per year: \n")
        [outputFileMessages.write(f"{key}: {value}\n") for key, value in years.items()]
        outputFileMessages.write("\n")

        outputFileMessages.write("Messages per month: \n")
        [outputFileMessages.write(f"{key}: {value}\n") for key, value in months.items()]
        outputFileMessages.write("\n")

        outputFileMessages.write("Messages per day: \n")
        [outputFileMessages.write(f"{key}: {value}\n") for key, value in days.items()]
        outputFileMessages.write("\n")

        outputFileMessages.write("Days with most messages: \n")
        i = 0
        for key, value in sorted(days.items(), key=lambda x: x[1], reverse=True):
            if i == 15:
                break
            outputFileMessages.write(f"{key}: {value}\n")
            i += 1
        outputFileMessages.write("\n")

        outputFileMessages.write("Messages per day of the week: \n")
        daysNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day, num in zip(daysNames, dayOfTheWeek):
            outputFileMessages.write(f"{day}: {num}\n")
        outputFileMessages.write("\n")

        outputFileMessages.write("Messages per hour of day: \n")
        for i in range(24):
            if i < 12:
                outputFileMessages.write(f"{(i + 11) % 12 + 1}AM: {hourOfTheDay[i]}\n")
            else:
                outputFileMessages.write(f"{(i + 11) % 12 + 1}PM: {hourOfTheDay[i]}\n")
        outputFileMessages.write("\n")

    with open("Stats/Words.txt", "a", encoding="utf8") as outputFileWords:
        outputFileWords.write("Number of words: ")
        last = 0
        for key, value in sorted(words.items(), key=lambda x: x[1], reverse=True):
            if value < 10:
                break
            if value == last:
                outputFileWords.write(f", {key}")
            else:
                outputFileWords.write(f"\n{value}: {key}")
                last = value
        outputFileWords.write("\n\n")

        last = 0
        outputFileWords.write("Number of words per user: \n")
        for key1, value1 in sorted(perUser.items(), key=lambda x: x[1][1], reverse=True):
            outputFileWords.write(f"{key1}:")
            for key2, value2 in sorted(value1[6].items(), key=lambda x: x[1], reverse=True):
                if value2 < 10:
                    break
                if value2 == last:
                    outputFileWords.write(f", {key2}")
                else:
                    outputFileWords.write(f"\n{value2}: {key2}")
                    last = value2
            outputFileWords.write("\n\n")

        outputFileWords.write("Number of unique words per user: \n")
        for key1, value1 in sorted(perUser.items(), key=lambda x: x[1][1], reverse=True):
            outputFileWords.write(f"{key1}: {len(value1[6].items())}\n")
        outputFileWords.write("\n")

    with open("Stats/Emojis.txt", "a", encoding="utf8") as outputFileEmojis:
        outputFileEmojis.write("Emojis: \n")
        for key, value in sorted(emojis.items(), key=lambda x: x[1], reverse=True):
            outputFileEmojis.write(f"{emojize(key)} : {value}\n")
        outputFileEmojis.write("\n")

        outputFileEmojis.write("Number of emojis per user: \n")
        [outputFileEmojis.write(f"{key}: {value[4]}\n") for key, value in sorted(perUser.items(), key=lambda x: x[1][4], reverse=True)]
        outputFileEmojis.write("\n")

        outputFileEmojis.write("Emojis per user: \n")
        for key1, value1 in sorted(perUser.items(), key=lambda x: x[1][4], reverse=True):
            outputFileEmojis.write(f"{key1}:\n")
            for key2, value2 in sorted(value1[5].items(), key=lambda x: x[1], reverse=True):
                outputFileEmojis.write(f"{emojize(key2)} : {value2}\n")
            outputFileEmojis.write("\n")
