import sys

from gui import *
# review
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec()
