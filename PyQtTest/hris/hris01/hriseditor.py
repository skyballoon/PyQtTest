#!/usr/bin/python
'''
Created on Jul 22, 2014

@author: pandazen.wordpress.com
'''

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox,
        QHBoxLayout, QPushButton, QTableView)
from PyQt5.QtSql import QSqlTableModel

class TableEditor(QDialog):
    def __init__(self, tableName, parent=None):
        super(TableEditor, self).__init__(parent)

        self.model = QSqlTableModel(self)
        self.model.setTable(tableName)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "First name")
        self.model.setHeaderData(2, Qt.Horizontal, "Last name")

        view = QTableView()
        view.setModel(self.model)

        submitButton = QPushButton("Submit")
        submitButton.setDefault(True)
        revertButton = QPushButton("&Revert")
        quitButton = QPushButton("Quit")

        buttonBox = QDialogButtonBox(Qt.Vertical)
        buttonBox.addButton(submitButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(revertButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QDialogButtonBox.RejectRole)

        #submitButton.clicked.connect(self.submit)
        #revertButton.clicked.connect(self.model.revertAll)
        #quitButton.clicked.connect(self.close)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(view)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Cached Table")