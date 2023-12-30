import sys

from gui import *
from input import *
from data import *
from output import *


def work(chat):
    removeOldFiles(chat)
    mergeNewFiles(chat)
    data = readData(chat)

    processedData = dataProcessing(data)

    writeData(chat, *processedData)


if __name__ == '__main__':
    app = QApplication("main.py")
    window = MyApp()
    window.show()
    app.exec()
