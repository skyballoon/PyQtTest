# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

from PyQt5 import QtCore, QtGui, QtWidgets


class HeaderView(QtWidgets.QHeaderView):

    rightButtonPressed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(HeaderView, self).__init__(QtCore.Qt.Horizontal, parent)
        self.setMovable(True)
        self.setClickable(True)
        self.setSortIndicatorShown(True)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.rightButtonPressed.emit()
            event.accept()
        else:
            QtGui.QHeaderView.mousePressEvent(self, event)


class TableView(QtWidgets.QTableView):

    rowSelected = QtCore.pyqtSignal(QtCore.QModelIndex)
    rightButtonPressed = QtCore.pyqtSignal(QtCore.QModelIndex)

    def __init__(self, parent=None):
        super(TableView, self).__init__(parent)
        header = HeaderView(self)
        header.rightButtonPressed.connect(self.on_header_rightButtonPressed)
        header.setSortIndicator(-1, QtCore.Qt.AscendingOrder)
        self.setHorizontalHeader(header)
        self.verticalHeader().hide()
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)

    def selectionChanged(self, selected, deselected):
        QtGui.QTableView.selectionChanged(self, selected, deselected)
        if selected.indexes():
            self.rowSelected.emit(selected.indexes()[0])

    def on_header_rightButtonPressed(self):
        header = self.horizontalHeader()
        menu = QtGui.QMenu()
        if header.sortIndicatorSection() != -1:
            a = menu.addAction(self.tr("Unsorted"))
            a.triggered.connect(self.on_unsorted_triggered)
            menu.addSeparator()
        group = QtGui.QActionGroup(menu)
        group.setExclusive(False)
        group.triggered.connect(self.on_action_triggered)
        for index in range(header.count()):
            text = self.model().headerData(index, QtCore.Qt.Horizontal).toString()
            a = menu.addAction(text)
            a.setCheckable(True)
            a.index = index
            a.setChecked(not (self.isColumnHidden(index) or
                              header.sectionSize(index) == 0))
            group.addAction(a)
        menu.exec_(QtGui.QCursor.pos())

    def on_action_triggered(self, action):
        self.setColumnHidden(action.index, not action.isChecked())
        header = self.horizontalHeader()
        if action.isChecked() and header.sectionSize(action.index) == 0:
            header.resizeSection(action.index, header.defaultSectionSize())

    def on_unsorted_triggered(self, checked):
        self.horizontalHeader().setSortIndicator(-1, QtCore.Qt.AscendingOrder)
        self.model().undoSorting()

    def mousePressEvent(self, event):
        pressed = False
        if event.button() == QtCore.Qt.RightButton:
            index = self.indexAt(event.pos())
            pressed = True

        QtGui.QTableView.mousePressEvent(self, event)

        if pressed:
            self.rightButtonPressed.emit(index)

