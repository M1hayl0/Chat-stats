from PySide6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QPushButton, QWidget, QLineEdit, QLabel, \
    QHBoxLayout, QTabWidget, QTextEdit
from PySide6.QtCore import QSize, Qt
import os
from main import work


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.numOfFiles = {}

        self.setWindowTitle("WhatsApp Stats")
        self.setFixedSize(QSize(800, 600))

        self.allTabs = QTabWidget()

        self.tabInput = QWidget()
        self.tabGeneral = QWidget()
        self.tabMessages = QWidget()
        self.tabWords = QWidget()
        self.tabEmojis = QWidget()

        # tabInput
        self.chatNameLabel = QLabel("Unesite ime chat-a: ")
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

        self.runButton = QPushButton('Run')
        self.runButton.setFixedSize(QSize(100, 50))
        self.runButton.clicked.connect(self.work)

        self.runBox = QHBoxLayout()
        self.runBox.addWidget(self.runButton, alignment=Qt.AlignCenter)

        self.tabInputLayout = QVBoxLayout(self.tabInput)
        self.tabInputLayout.addLayout(self.chatNameInputBox)
        self.tabInputLayout.addLayout(self.importFileBox)
        self.tabInputLayout.addLayout(self.runBox)

        # tabGeneral
        self.textEditGeneral = QTextEdit()
        self.textEditGeneral.setReadOnly(True)
        self.tabGeneralLayout = QVBoxLayout(self.tabGeneral)
        self.tabGeneralLayout.addWidget(self.textEditGeneral)

        # tabMessages
        self.textEditMessages = QTextEdit()
        self.textEditMessages.setReadOnly(True)
        self.tabMessagesLayout = QVBoxLayout(self.tabMessages)
        self.tabMessagesLayout.addWidget(self.textEditMessages)

        # tabWords
        self.textEditWords = QTextEdit()
        self.textEditWords.setReadOnly(True)
        self.tabWordslLayout = QVBoxLayout(self.tabWords)
        self.tabWordslLayout.addWidget(self.textEditWords)

        # tabEmojis
        self.textEditEmojis = QTextEdit()
        self.textEditEmojis.setReadOnly(True)
        self.tabEmojisLayout = QVBoxLayout(self.tabEmojis)
        self.tabEmojisLayout.addWidget(self.textEditEmojis)

        self.allTabs.addTab(self.tabInput, "Input")
        self.allTabs.addTab(self.tabGeneral, "General")
        self.allTabs.addTab(self.tabMessages, "Messages")
        self.allTabs.addTab(self.tabWords, "Words")
        self.allTabs.addTab(self.tabEmojis, "Emojis")

        layout = QVBoxLayout()
        layout.addWidget(self.allTabs)
        self.setLayout(layout)

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Import File", "D:", "Files (*.txt)", options=options)
        if fileName:
            with open(fileName, 'r') as f:
                data = f.read()
                chat = self.chatNameInput.text()
                if not os.path.exists(f"Input/{chat}"):
                    os.mkdir(f"Input/{chat}")
                    self.numOfFiles[chat] = 0
                with open(f"Input/{chat}/{chat}{self.numOfFiles[chat]}.txt", 'a') as f2:
                    f2.write(data)
                self.numOfFiles[chat] += 1

    def work(self):
        chat = self.chatNameInput.text()
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
