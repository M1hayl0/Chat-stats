import time
from input import *
from data import *
from output import *

start = time.time()
if __name__ == '__main__':
    chat = "person"

    removeOldFiles(chat)
    mergeNewFiles(chat)
    data = readData(chat)

    processedData = dataProcessing(data)

    writeData(chat, *processedData)

    end = time.time()
    print(end - start)

