from PySide6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QPushButton, QWidget, QLineEdit, QLabel, \
    QHBoxLayout, QTabWidget, QTextEdit, QListWidget
from PySide6.QtCore import QSize, Qt
import os

from main import work
from input import addToDatabase

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WhatsApp Stats")
        self.setFixedSize(QSize(800, 600))

        self.allTabs = QTabWidget()
        self.tabWidgets = {
            "Input": self.initInputTab,
            "Run": self.initRunTab,
            "General": self.initGeneralTab,
            "Messages": self.initMessagesTab,
            "Words": self.initWordsTab,
            "Emojis": self.initEmojisTab
        }

        for tabName, initMethod in self.tabWidgets.items():
            tab = QWidget()
            initMethod(tab)
            self.allTabs.addTab(tab, tabName)

        layout = QVBoxLayout()
        layout.addWidget(self.allTabs)
        self.setLayout(layout)

    def initInputTab(self, tabInput):
        self.chatNameLabel = QLabel("Enter chat name: ")
        self.chatNameLabel.setFixedSize(QSize(170, 40))
        self.chatNameLabel.setAlignment(Qt.AlignCenter)

        self.chatNameInput = QLineEdit()
        self.chatNameInput.setPlaceholderText("person")
        self.chatNameInput.setFixedSize(QSize(170, 40))
        self.chatNameInput.setAlignment(Qt.AlignCenter)

        self.chatNameInputBox = QHBoxLayout()
        self.chatNameInputBox.addWidget(self.chatNameLabel, alignment=Qt.AlignCenter)
        self.chatNameInputBox.addWidget(self.chatNameInput, alignment=Qt.AlignCenter)

        self.importFileButton = QPushButton('Import Chat')
        self.importFileButton.setFixedSize(QSize(100, 50))
        self.importFileButton.clicked.connect(self.openFile)

        self.importFileBox = QHBoxLayout()
        self.importFileBox.addWidget(self.importFileButton, alignment=Qt.AlignCenter)

        self.tabInputLayout = QVBoxLayout(tabInput)
        self.tabInputLayout.addLayout(self.chatNameInputBox)
        self.tabInputLayout.addLayout(self.importFileBox)

    def initRunTab(self, tabRun):
        self.runButton = QPushButton('Run')
        self.runButton.setFixedSize(QSize(100, 50))
        self.runButton.clicked.connect(self.work)

        self.runChatsList = QListWidget()
        for chat in os.listdir("Input"):
            self.runChatsList.addItem(chat[:-3])
        self.runChatsList.setStyleSheet("QListWidget::item { min-height: 50px; }")

        self.tabRunLayout = QVBoxLayout(tabRun)
        self.tabRunLayout.addWidget(self.runChatsList)
        self.tabRunLayout.addWidget(self.runButton, alignment=Qt.AlignCenter)

    def initGeneralTab(self, tabGeneral):
        self.textEditGeneral = QTextEdit()
        self.textEditGeneral.setReadOnly(True)
        self.tabGeneralLayout = QVBoxLayout(tabGeneral)
        self.tabGeneralLayout.addWidget(self.textEditGeneral)

    def initMessagesTab(self, tabMessages):
        self.textEditMessages = QTextEdit()
        self.textEditMessages.setReadOnly(True)
        self.tabMessagesLayout = QVBoxLayout(tabMessages)
        self.tabMessagesLayout.addWidget(self.textEditMessages)

    def initWordsTab(self, tabWords):
        self.textEditWords = QTextEdit()
        self.textEditWords.setReadOnly(True)
        self.tabWordslLayout = QVBoxLayout(tabWords)
        self.tabWordslLayout.addWidget(self.textEditWords)

    def initEmojisTab(self, tabEmojis):
        self.textEditEmojis = QTextEdit()
        self.textEditEmojis.setReadOnly(True)
        self.tabEmojisLayout = QVBoxLayout(tabEmojis)
        self.tabEmojisLayout.addWidget(self.textEditEmojis)

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Import File", "D:", "Files (*.txt)", options=options)
        if fileName:
            with open(fileName, 'r', encoding="utf8") as f:
                data = f.read()
                chat = self.chatNameInput.text()
                if not os.path.exists(f"Input/{chat}.db"):
                    self.runChatsList.addItem(chat)
                    addToDatabase(chat, data, True)
                else:
                    addToDatabase(chat, data, False)

    def work(self):
        chat = self.runChatsList.selectedItems()[0].text()
        work(chat)
        with open("Stats/General.txt", "r", encoding="utf8") as outputFileGeneral:
            data = outputFileGeneral.read()
            self.textEditGeneral.setText(data)
        with open("Stats/Messages.txt", "r", encoding="utf8") as outputFileMessages:
            data = outputFileMessages.read()
            self.textEditMessages.setText(data)
        with open("Stats/Words.txt", "r", encoding="utf8") as outputFileWords:
            data = outputFileWords.read()
            self.textEditWords.setText(data)
        with open("Stats/Emojis.txt", "r", encoding="utf8") as outputFileEmojis:
            data = outputFileEmojis.read()
            self.textEditEmojis.setText(data)
