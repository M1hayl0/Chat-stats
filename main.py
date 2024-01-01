import sys

from gui import *
from input import *
from data import *
from output import *


def work(chat):
    removeOldFiles()
    processedData = dataProcessing(chat)
    writeData(chat, *processedData)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec()
