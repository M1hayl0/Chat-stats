from PySide6 import QtCore
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QPushButton, QWidget, QLineEdit, QLabel, \
    QHBoxLayout, QTabWidget, QTextEdit, QListWidget, QMessageBox, QDialog
from PySide6.QtCore import QSize, Qt, QThread, Signal
import os

from data import dataProcessing
from input import addToDatabase


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WhatsApp Stats")
        self.setFixedSize(QSize(800, 600))
        self.setStyleSheet("background-color: #25d366;")
        self.initDialog()

        self.allTabs = QTabWidget()
        self.allTabs.setFont(QFont("Helvetica", 10))
        self.tabWidgets = {
            "Import": self.initInputTab,
            "Run": self.initRunTab,
            "General": self.initGeneralTab,
            "Messages": self.initMessagesTab,
            "Words": self.initWordsTab,
            "Emojis": self.initEmojisTab
        }

        for tabName, initMethod in self.tabWidgets.items():
            tab = QWidget()
            tab.setStyleSheet("background-color: #ece5dd;")
            initMethod(tab)
            self.allTabs.addTab(tab, tabName)

        layout = QVBoxLayout()
        layout.addWidget(self.allTabs)
        self.setLayout(layout)

    def initInputTab(self, tabInput):
        self.chatNameLabel = QLabel("Enter chat name: ")
        self.chatNameLabel.setFixedSize(QSize(250, 50))
        self.chatNameLabel.setFont(QFont("Helvetica", 16))
        self.chatNameLabel.setStyleSheet("color: #075e54;")
        self.chatNameLabel.setAlignment(Qt.AlignCenter)

        self.chatNameInput = QLineEdit()
        self.chatNameInput.setFixedSize(QSize(250, 50))
        self.chatNameInput.setFont(QFont("Helvetica", 16))
        self.chatNameInput.setStyleSheet("color: #FFFFFF; background-color: #25d366;")

        self.chatNameInputBox = QHBoxLayout()
        self.chatNameInputBox.addWidget(self.chatNameLabel, alignment=Qt.AlignCenter)
        self.chatNameInputBox.addWidget(self.chatNameInput, alignment=Qt.AlignCenter)

        self.importFileButton = QPushButton("Import Chat")
        self.importFileButton.setFixedSize(QSize(150, 60))
        self.importFileButton.clicked.connect(self.openFile)
        self.importFileButton.setFont(QFont("Helvetica", 16))
        self.importFileButton.setStyleSheet("color: #FFFFFF; background-color: #25d366;")

        self.importFileBox = QHBoxLayout()
        self.importFileBox.addWidget(self.importFileButton, alignment=Qt.AlignCenter)

        self.tabInputLayout = QVBoxLayout(tabInput)
        self.tabInputLayout.addLayout(self.chatNameInputBox)
        self.tabInputLayout.addLayout(self.importFileBox)

    def initRunTab(self, tabRun):
        self.runButton = QPushButton('Run')
        self.runButton.setFixedSize(QSize(100, 50))
        self.runButton.clicked.connect(self.dataProcessing)
        self.runButton.setFont(QFont("Helvetica", 16))
        self.runButton.setStyleSheet("color: #FFFFFF; background-color: #25d366;")

        self.runChatsList = QListWidget()
        self.runChatsList.setFont(QFont("Helvetica", 12))
        for chat in os.listdir("Input"):
            self.runChatsList.addItem(chat[:-3])

        for i in range(self.runChatsList.count()):
            self.runChatsList.item(i).setBackground(QColor('#25d366'))

        self.runChatsList.setStyleSheet("""
            QListWidget::item { min-height: 50px; color: #FFFFFF; };
        """)
        self.runChatsList.itemSelectionChanged.connect(self.updateItemColors)

        self.tabRunLayout = QVBoxLayout(tabRun)
        self.tabRunLayout.addWidget(self.runChatsList)
        self.tabRunLayout.addWidget(self.runButton, alignment=Qt.AlignCenter)

    def updateItemColors(self):
        for i in range(self.runChatsList.count()):
            item = self.runChatsList.item(i)
            if item.isSelected():
                item.setBackground(QColor('#075e54'))
                item.setFont(QFont("Helvetica", 15))
            else:
                item.setBackground(QColor('#25d366'))
                item.setFont(QFont("Helvetica", 12))

    def initGeneralTab(self, tabGeneral):
        self.textEditGeneral = QTextEdit()
        self.textEditGeneral.setReadOnly(True)
        self.textEditGeneral.setFont(QFont("Helvetica", 12))
        self.textEditGeneral.setStyleSheet("color: #075e54;")
        self.tabGeneralLayout = QVBoxLayout(tabGeneral)
        self.tabGeneralLayout.addWidget(self.textEditGeneral)

    def initMessagesTab(self, tabMessages):
        self.textEditMessages = QTextEdit()
        self.textEditMessages.setReadOnly(True)
        self.textEditMessages.setFont(QFont("Helvetica", 12))
        self.textEditMessages.setStyleSheet("color: #075e54;")
        self.tabMessagesLayout = QVBoxLayout(tabMessages)
        self.tabMessagesLayout.addWidget(self.textEditMessages)

    def initWordsTab(self, tabWords):
        self.textEditWords = QTextEdit()
        self.textEditWords.setReadOnly(True)
        self.textEditWords.setFont(QFont("Helvetica", 12))
        self.textEditWords.setStyleSheet("color: #075e54;")
        self.tabWordslLayout = QVBoxLayout(tabWords)
        self.tabWordslLayout.addWidget(self.textEditWords)

    def initEmojisTab(self, tabEmojis):
        self.textEditEmojis = QTextEdit()
        self.textEditEmojis.setReadOnly(True)
        self.textEditEmojis.setFont(QFont("Helvetica", 12))
        self.textEditEmojis.setStyleSheet("color: #075e54;")
        self.tabEmojisLayout = QVBoxLayout(tabEmojis)
        self.tabEmojisLayout.addWidget(self.textEditEmojis)

    def initDialog(self):
        self.importDialog = QDialog(self)
        self.importDialog.setWindowFlags(self.importDialog.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.importDialog.setFixedSize(QSize(200, 100))
        self.importDialog.setStyleSheet("background-color: #ece5dd;")
        self.importDialog.setWindowTitle("WhatsApp Stats")
        importDialogLayout = QVBoxLayout()
        self.importDialogText = QLabel("Importing data...")
        self.importDialogText.setFont(QFont("Helvetica", 12))
        self.importDialogText.setStyleSheet("color: #075e54")
        importDialogLayout.addWidget(self.importDialogText, alignment=Qt.AlignCenter)
        self.importDialog.setLayout(importDialogLayout)

        self.runDialog = QDialog(self)
        self.runDialog.setWindowFlags(self.runDialog.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.runDialog.setFixedSize(QSize(200, 100))
        self.runDialog.setStyleSheet("background-color: #ece5dd;")
        self.runDialog.setWindowTitle("WhatsApp Stats")
        runDialogLayout = QVBoxLayout()
        self.runDialogText = QLabel("Data processing...")
        self.runDialogText.setFont(QFont("Helvetica", 12))
        self.runDialogText.setStyleSheet("color: #075e54")
        runDialogLayout.addWidget(self.runDialogText, alignment=Qt.AlignCenter)
        self.runDialog.setLayout(runDialogLayout)

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Import File", "D:", "Files (*.txt)", options=options)
        if fileName:
            with open(fileName, 'r', encoding="utf8") as f:
                data = f.read()
                chat = self.chatNameInput.text()
                if not os.path.exists(f"Input/{chat}.db"):
                    self.dbWorker = addToDatabaseWorker(chat, data, True)
                else:
                    self.removeFromChatList(chat)
                    self.dbWorker = addToDatabaseWorker(chat, data, False)
                self.dbWorker.finished.connect(self.addToChatList)
                self.dbWorker.start()
                self.importDialog.show()

    def addToChatList(self, chat):
        self.importDialog.close()
        self.runChatsList.addItem(chat)
        self.updateItemColors()

    def removeFromChatList(self, chat):
        item = self.runChatsList.findItems(chat, QtCore.Qt.MatchExactly)
        self.runChatsList.takeItem(self.runChatsList.row(item[0]))

    def dataProcessing(self):
        chat = self.runChatsList.selectedItems()[0].text()
        self.worker = dataProcessingWorker(chat)
        self.worker.finished.connect(self.output)
        self.worker.start()
        self.runDialog.show()

    def output(self, chat):
        with open(f"Output/{chat}/General.txt", "r", encoding="utf8") as outputFileGeneral:
            data = outputFileGeneral.read()
            self.textEditGeneral.setText(data)
        with open(f"Output/{chat}/Messages.txt", "r", encoding="utf8") as outputFileMessages:
            data = outputFileMessages.read()
            self.textEditMessages.setText(data)
        with open(f"Output/{chat}/Words.txt", "r", encoding="utf8") as outputFileWords:
            data = outputFileWords.read()
            self.textEditWords.setText(data)
        with open(f"Output/{chat}/Emojis.txt", "r", encoding="utf8") as outputFileEmojis:
            data = outputFileEmojis.read()
            self.textEditEmojis.setText(data)
        self.runDialog.close()


class dataProcessingWorker(QThread):
    finished = Signal(str)

    def __init__(self, chat):
        super().__init__()
        self.chat = chat

    def run(self):
        dataProcessing(self.chat)
        self.finished.emit(self.chat)


class addToDatabaseWorker(QThread):
    finished = Signal(str)

    def __init__(self, chat, data, first):
        super().__init__()
        self.chat = chat
        self.data = data
        self.first = first

    def run(self):
        addToDatabase(self.chat, self.data, self.first)
        self.finished.emit(self.chat)
