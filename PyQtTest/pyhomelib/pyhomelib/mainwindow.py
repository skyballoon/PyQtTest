# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et tw=79 sts=4 ai si

import os
import sys
import shlex

from PyQt5 import QtCore, QtSql, QtWidgets, QtGui

from ui.mainwindow import Ui_MainWindow

from dbpropertiesdialog import DbPropertiesDialog
from windowstatereader import WindowStateReader
from windowstatewriter import WindowStateWriter
from genretreemodelreader import GenreTreeModelReader
from bookdblayer import BookDbLayer
from fb2streamreader import FB2StreamReader
from fb2bookparserthread import FB2BookParserThread
from sqlquerymodel import SqlQueryModel
from settingsdialog import SettingsDialog
from statisticsdialog import StatisticsDialog
from mysettings import MySettings
from importdialog import ImportDialog


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow,
                 WindowStateReader, WindowStateWriter):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        WindowStateReader.__init__(self)
        WindowStateWriter.__init__(self)
        self._db = BookDbLayer()

        self.userConfigDir = QtCore.QDir.homePath() + QtCore.QDir.separator() + \
                             '.pyhomelib';
        if not QtCore.QFileInfo(self.userConfigDir).isDir():
            QtCore.QDir.home().mkdir('.pyhomelib')
        self.uiSettingsFile = self.userConfigDir + QtCore.QDir.separator() + \
                              'ui.xml'
        self.programSettings = MySettings(self.userConfigDir +
                                          QtCore.QDir.separator() +
                                          'pyhomelib.conf')

        if len(sys.argv) < 2:
            dbname = self.userConfigDir + QtCore.QDir.separator() + \
                     'default.sqlite'
        else:
            dbname = QtCore.QString.fromUtf8(sys.argv[1])

        genreModel = GenreTreeModelReader('genres.xml')

        info = QtCore.QFileInfo(dbname)
        if info.exists() and info.size() > 0:
            self._db.open(dbname)
        else:
            QtGui.QMessageBox.information(self, self.tr("Information"),
                QtCore.QString(self.tr("Database doesn't exists, recreating: %1"))
                .arg(dbname))
            self._db.create(dbname, 'Default', '', genreModel.list(),
                     [self.tr('Favorites')])

        try:
            import sqlite3ext
            handle = db().driver().handle()
            sqlite3ext.load_icu(handle.data().ascobject())
        except ImportError:
            pass

        self.setupUi(self)
        QtGui.qApp.setStyleSheet(QtCore.QResource(":resources/pyhomelib.css").data())
        self.appTitle = self.windowTitle()
        self.prependToTitle(self._db.getDbProperty('name').toString())
        self.actionRuLetterA.setText(u"А")
        self.actionRuLetterB.setText(u"Б")
        self.actionRuLetterV.setText(u"В")
        self.actionRuLetterG.setText(u"Г")
        self.actionRuLetterD.setText(u"Д")
        self.actionRuLetterE.setText(u"Е")
        self.actionRuLetterYo.setText(u"Ё")
        self.actionRuLetterZh.setText(u"Ж")
        self.actionRuLetterZ.setText(u"З")
        self.actionRuLetterI.setText(u"И")
        self.actionRuLetterY.setText(u"Й")
        self.actionRuLetterK.setText(u"К")
        self.actionRuLetterL.setText(u"Л")
        self.actionRuLetterM.setText(u"М")
        self.actionRuLetterN.setText(u"Н")
        self.actionRuLetterO.setText(u"О")
        self.actionRuLetterP.setText(u"П")
        self.actionRuLetterR.setText(u"Р")
        self.actionRuLetterS.setText(u"С")
        self.actionRuLetterT.setText(u"Т")
        self.actionRuLetterU.setText(u"У")
        self.actionRuLetterF.setText(u"Ф")
        self.actionRuLetterH.setText(u"Х")
        self.actionRuLetterTs.setText(u"Ц")
        self.actionRuLetterCh.setText(u"Ч")
        self.actionRuLetterSh.setText(u"Ш")
        self.actionRuLetterSch.setText(u"Щ")
        self.actionRuLetterYy.setText(u"Ы")
        self.actionRuLetterEe.setText(u"Э")
        self.actionRuLetterYu.setText(u"Ю")
        self.actionRuLetterYa.setText(u"Я")

        self.lettersGroup = QtGui.QActionGroup(self)
        for a in self.findChildren(QtGui.QAction):
            if a.objectName().startsWith('actionRuLetter') or \
               a.objectName().startsWith('actionEnLetter'):
                self.lettersGroup.addAction(a)

        self.authorsModel = SqlQueryModel(self, self._db, "authorid, lastname, firstname",
                                                          "libauthorname",
                                                          None,
                                                          "lastname, firstname")
        self.authorsView.setModel(self.authorsModel)
        self.setTableAuthorsModelQuery()
        self.authorsView.hideColumn(0)
        for index, name in enumerate([self.tr("authorid"),
                                      self.tr("Last name"),
                                      self.tr("First name")]):
            self.authorsView.model().setHeaderData(index, QtCore.Qt.Horizontal, name)

        self.sequencesModel = SqlQueryModel(self, self._db, "seqid, seqname",
                                                            "libseqname",
                                                            None,
                                                            "seqname")
        self.sequencesView.setModel(self.sequencesModel)
        self.sequencesModel.select()
        self.sequencesView.hideColumn(0)
        for index, name in enumerate([self.tr("seqid"),
                                      self.tr("Sequence")]):
            self.sequencesView.model().setHeaderData(index, QtCore.Qt.Horizontal, name)

        self.genresTree.setModel(genreModel)
        self.genresTree.hideColumn(1)


        self.bookSearchModel = SqlQueryModel(self, self._db, "b.bookid, firstname, lastname, title, seqname, genredesc, lang, year",
                                                             "libbook b LEFT JOIN libsequence s ON b.bookid = s.bookid LEFT JOIN libseqname sn ON s.seqid = sn.seqid LEFT JOIN libauthor a ON b.bookid = a.bookid LEFT JOIN libauthorname an ON a.authorid = an.authorid LEFT JOIN libgenre g ON b.bookid = g.bookid LEFT JOIN libgenrelist gl ON g.genreid = gl.genreid",
                                                             "b.bookid = 0",
                                                             None,
                                                             "1")
        self.bookSearchView.setModel(self.bookSearchModel)
        self.bookSearchModel.select()
        self.bookSearchView.hideColumn(0)
        for index, name in enumerate([self.tr("bookid"),
                                      self.tr("First name"),
                                      self.tr("Last name"),
                                      self.tr("Book Title"),
                                      self.tr("Sequence"),
                                      self.tr("Genre"),
                                      self.tr("Lang"),
                                      self.tr("Year")]):
            self.bookSearchModel.setHeaderData(index, QtCore.Qt.Horizontal, name)

        self.groupsModel = SqlQueryModel(self, self._db, "groupid, groupname",
                                                         "libgrouplist",
                                                         None,
                                                         "groupname")
        self.groupsView.setModel(self.groupsModel)
        self.groupsModel.select()
        self.groupsView.hideColumn(0)
        for index, name in enumerate([self.tr("groupid"),
                                      self.tr("Group")]):
            self.groupsView.model().setHeaderData(index, QtCore.Qt.Horizontal, name)

        self.booksByAuthorModel = SqlQueryModel(self, self._db, "bookid, title, seqname, genredesc, lang, year",
                                                                "libauthor a INNER JOIN libbook b USING(bookid) LEFT JOIN libseqname s ON b.seqid = s.seqid LEFT JOIN libgenrelist g ON b.genreid = g.genreid",
                                                                "a.authorid = ?")
        self.booksByAuthorView.setModel(self.booksByAuthorModel)
        self.booksByAuthorModel.addBindValue(0)
        self.booksByAuthorModel.select()
        self.booksByAuthorView.hideColumn(0)
        for index, name in enumerate([self.tr("bookid"),
                                      self.tr("Book Title"),
                                      self.tr("Sequence"),
                                      self.tr("Genre"),
                                      self.tr("Lang"),
                                      self.tr("Year")]):
            self.booksByAuthorModel.setHeaderData(index, QtCore.Qt.Horizontal, name)

        self.booksBySeqModel = SqlQueryModel(self, self._db, "bookid, firstname, lastname, title, genredesc, lang, year",
                                                             "libsequence s INNER JOIN libbook b USING(bookid) LEFT JOIN libauthorname a ON b.authorid = a.authorid LEFT JOIN libgenrelist g ON b.genreid = g.genreid",
                                                             "s.seqid = ?")
        self.booksBySeqView.setModel(self.booksBySeqModel)
        self.booksBySeqModel.addBindValue(0)
        self.booksBySeqModel.select()
        self.booksBySeqView.hideColumn(0)
        for index, name in enumerate([self.tr("bookid"),
                                      self.tr("First name"),
                                      self.tr("Last name"),
                                      self.tr("Book Title"),
                                      self.tr("Genre"),
                                      self.tr("Lang"),
                                      self.tr("Year")]):
            self.booksBySeqModel.setHeaderData(index, QtCore.Qt.Horizontal, name)

        self.booksByGenreModel = SqlQueryModel(self, self._db, "bookid, firstname, lastname, title, seqname, lang, year",
                                                               "libgenre g INNER JOIN libbook b USING(bookid) LEFT JOIN libauthorname a ON b.authorid = a.authorid LEFT JOIN libseqname s ON b.seqid = s.seqid",
                                                               "g.genreid = ?")
        self.booksByGenreView.setModel(self.booksByGenreModel)
        self.booksByGenreModel.addBindValue(0)
        self.booksByGenreModel.select()
        self.booksByGenreView.hideColumn(0)
        for index, name in enumerate([self.tr("bookid"),
                                      self.tr("First name"),
                                      self.tr("Last name"),
                                      self.tr("Book Title"),
                                      self.tr("Sequence"),
                                      self.tr("Lang"),
                                      self.tr("Year")]):
            self.booksByGenreModel.setHeaderData(index, QtCore.Qt.Horizontal, name)

        self.booksByGroupModel = SqlQueryModel(self, self._db, "b.bookid, firstname, lastname, title, seqname, genredesc, lang, year",
                                                               "libgroup g INNER JOIN libbook b USING(bookid) LEFT JOIN libseqname s ON b.seqid = s.seqid LEFT JOIN libauthorname a ON b.authorid = a.authorid LEFT JOIN libgenrelist gl ON b.genreid = gl.genreid",
                                                               "g.groupid = ?")
        self.booksByGroupView.setModel(self.booksByGroupModel)
        self.booksByGroupModel.addBindValue(0)
        self.booksByGroupModel.select()
        self.booksByGroupView.hideColumn(0)
        for index, name in enumerate([self.tr("bookid"),
                                      self.tr("First name"),
                                      self.tr("Last name"),
                                      self.tr("Book Title"),
                                      self.tr("Sequence"),
                                      self.tr("Genre"),
                                      self.tr("Lang"),
                                      self.tr("Year")]):
            self.booksByGroupModel.setHeaderData(index, QtCore.Qt.Horizontal, name)

        self.readStateFrom(self.uiSettingsFile)
        self.actionRussianAlphabet.setChecked(self.ruLettersToolbar.isVisibleTo(self))
        self.actionEnglishAlphabet.setChecked(self.enLettersToolbar.isVisibleTo(self))

        if not self.programSettings.getRowHeight():
            self.programSettings.writeRowHeight(self.authorsView.verticalHeader().defaultSectionSize())
        else:
            self.setRowHeight(self.programSettings.getRowHeight())

        for key in ('/', 'Ctrl+F'):
            QtGui.QShortcut(key, self).activated.connect(self.on_quickFindShortcut_activated)

        self.parserThread = FB2BookParserThread()
        self.parserThread.bookParsed.connect(self.bookParsed)
        self.parserThread.start()

    def __del__(self):
        self.parserThread.wait()

    def on_ruLettersToolbar_actionTriggered(self, action):
        self.setTableAuthorsModelQuery()

    def on_enLettersToolbar_actionTriggered(self, action):
        self.setTableAuthorsModelQuery()

    def on_authorEdit_textChanged(self, text):
        self.setTableAuthorsModelQuery()

    def on_sequenceEdit_textChanged(self, text):
        self.setTableSequencesModelQuery()

    def setTableAuthorsModelQuery(self):
        model = self.authorsModel
        if not self.authorEdit.text().isEmpty():
            model.setWhereClause("lastname LIKE ?")
            model.addBindValue(self.authorEdit.text() + "%")
        else:
            checkedLetter = self.lettersGroup.checkedAction()
            if checkedLetter and checkedLetter.text() != '*':
                model.setWhereClause("lastname LIKE ?")
                model.addBindValue(checkedLetter.text() + "%")
            else:
                model.setWhereClause(None)
        model.select()

    def setTableSequencesModelQuery(self):
        model = self.sequencesModel
        if self.sequenceEdit.text().isEmpty():
            model.setWhereClause(None)
        else:
            model.setWhereClause("seqname LIKE ?")
            model.addBindValue(self.sequenceEdit.text() + "%")
        model.select()

    def on_authorsView_rowSelected(self, index):
        model = self.authorsModel
        authorid = model.record(index.row()).value(0).toInt()[0]
        text = model.record(index.row()).value(2).toString().append(" ") + \
               model.record(index.row()).value(1).toString()
        self.authorTitleLabel.setText(text)
        self.booksByAuthorModel.addBindValue(authorid)
        self.booksByAuthorModel.select()

    def on_sequencesView_rowSelected(self, index):
        model = self.sequencesModel
        seqid = model.record(index.row()).value(0).toInt()[0]
        text = model.record(index.row()).value(1).toString()
        self.seqTitleLabel.setText(text)
        self.booksBySeqModel.addBindValue(seqid)
        self.booksBySeqModel.select()

    def on_genresTree_rowSelected(self, index):
        model = self.genresTree.model()
        genredesc = model.data(index)
        newidx = model.index(index.row(), 1, index.parent())
        genreid = model.data(newidx)
        self.genreTitleLabel.setText(genredesc)
        self.booksByGenreModel.addBindValue(genreid)
        self.booksByGenreModel.select()

    def on_groupsView_rowSelected(self, index):
        model = self.groupsModel
        groupid = model.record(index.row()).value(0).toInt()[0]
        text = model.record(index.row()).value(1).toString()
        self.groupTitleLabel.setText(text)
        self.booksByGroupModel.addBindValue(groupid)
        self.booksByGroupModel.select()

    def prependToTitle(self, str):
        self.setWindowTitle(str + " - " + self.appTitle)

    def closeEvent(self, event):
        self.parserThread.quit()
        if self.programSettings.getSaveUiOnExitOption():
            self.writeStateTo(self.uiSettingsFile)
        event.accept()

    @QtCore.pyqtSlot()
    def on_actionDbProperties_triggered(self):
        dialog = DbPropertiesDialog(self._db, self)
        dialog.nameEdit.setFocus()
        if dialog.exec_():
            self.prependToTitle(self._db.getDbProperty('name').toString())

    @QtCore.pyqtSlot()
    def on_actionDbScanBookDir_triggered(self):
        dirname = QtGui.QFileDialog.getExistingDirectory(self,
                                            self.tr("Select directory"),
                                            QtCore.QDir.homePath(),
                                            QtGui.QFileDialog.ShowDirsOnly)
        if not dirname.isEmpty():
            self._db.finishActiveQueries()
            dlg = ImportDialog(QtCore.QDir(dirname).absolutePath(),
                               self)
            dlg.exec_()
            for widget in self.findChildren(QtGui.QTableView):
                widget.model().refresh()
                QtGui.qApp.processEvents()


    def bookParsed(self, reader):
        label = self.coverpageLabel
        edit = self.annotationEdit
        if reader.hasError():
            label.setText(self.tr("Parser error"))
            edit.setText("")
        else:
            edit.setText(reader.info.Annotation)
            if reader.info.Coverpage.isEmpty() or reader.info.Coverpage.size() <= 120:
                label.setText(self.tr("No coverpage"))
            else:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(reader.info.Coverpage)
                if pixmap.width() <= 200:
                    label.setPixmap(pixmap)
                else:
                    label.setPixmap(pixmap.scaledToWidth(200, QtCore.Qt.SmoothTransformation))

    def on_booksByAuthorView_rowSelected(self, index):
        model = self.booksByAuthorModel
        if self.dockWidget.isVisible():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksBySeqView_rowSelected(self, index):
        model = self.booksBySeqModel
        if self.dockWidget.isVisible():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_bookSearchView_rowSelected(self, index):
        model = self.bookSearchModel
        if self.dockWidget.isVisible():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksByGenreView_rowSelected(self, index):
        model = self.booksByGenreModel
        if self.dockWidget.isVisible():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksByGroupView_rowSelected(self, index):
        model = self.booksByGroupModel
        if self.dockWidget.isVisible():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksByAuthorView_doubleClicked(self, index):
        model = self.booksByAuthorModel
        bookid = model.record(index.row()).value(0).toInt()[0]
        self.startDefaultProgramUsingBookId(bookid)

    def on_booksBySeqView_doubleClicked(self, index):
        model = self.booksBySeqModel
        bookid = model.record(index.row()).value(0).toInt()[0]
        self.startDefaultProgramUsingBookId(bookid)

    def on_booksByGenreView_doubleClicked(self, index):
        model = self.booksByGenreModel
        bookid = model.record(index.row()).value(0).toInt()[0]
        self.startDefaultProgramUsingBookId(bookid)

    def on_bookSearchView_doubleClicked(self, index):
        model = self.bookSearchModel
        bookid = model.record(index.row()).value(0).toInt()[0]
        self.startDefaultProgramUsingBookId(bookid)

    def on_booksByGroupView_doubleClicked(self, index):
        model = self.booksByGroupModel
        bookid = model.record(index.row()).value(0).toInt()[0]
        self.startDefaultProgramUsingBookId(bookid)

    def startDefaultProgramUsingBookId(self, bookid):
        filename = self._db.getFilenameByBookId(bookid)
        if filename:
            programs = self.programSettings.getPrograms()
            if programs:
                args = [x.decode('utf8') for x in
                        shlex.split(unicode(programs[0][1]).encode('utf8'))]
                if args:
                    program = args.pop(0)
                    args = [arg.replace('%p', filename) for arg in args]
                    self.startProgramDetached(program, args)

    def startProgramDetached(self, program, args):
        if not QtCore.QProcess.startDetached(program, args):
            QtGui.QMessageBox.critical(self, self.tr("Error"),
                    QtCore.QString(self.tr("Unable to start program: %1"))
                    .arg(program))

    @QtCore.pyqtSlot()
    def on_actionConfigure_triggered(self):
        dialog = SettingsDialog(self.programSettings, self)
        dialog.rowHeightChanged.connect(self.setRowHeight)
        dialog.exec_()

    @QtCore.pyqtSlot(int)
    def setRowHeight(self, value):
        for view in self.findChildren(QtGui.QTableView):
            view.verticalHeader().setDefaultSectionSize(value)

    def makePopupMenu(self, bookid):
        menu = QtGui.QMenu()
        if bookid:
            filename = self._db.getFilenameByBookId(bookid)
            group = QtGui.QActionGroup(menu)
            group.triggered.connect(self.on_group1_triggered)
            for program in self.programSettings.getPrograms():
                if not program[1].isEmpty():
                    if program[0].isEmpty():
                        a = menu.addAction(program[1])
                    else:
                        a = menu.addAction(program[0])
                    args = [x.decode('utf8') for x in
                            shlex.split(unicode(program[1]).encode('utf8'))]
                    program = args.pop(0)
                    args = [arg.replace('%p', filename) for arg in args]
                    a.program = program
                    a.args = args
                    group.addAction(a)
            groups = self._db.getGroupsBookNotIn(bookid)
            if groups:
                if not menu.isEmpty():
                    menu.addSeparator()
                menu2 = QtGui.QMenu(self.tr("Add to group"), menu)
                group2 = QtGui.QActionGroup(menu2)
                group2.triggered.connect(self.on_group2_triggered)
                for group in groups:
                    a = menu2.addAction(group[1])
                    a.bookid = bookid
                    a.groupid = group[0]
                    group2.addAction(a)
                menu.addMenu(menu2)
            groups = self._db.getGroupsBookIn(bookid)
            if groups:
                if not menu.isEmpty():
                    menu.addSeparator()
                menu3 = QtGui.QMenu(self.tr("Remove from group"), menu)
                group3 = QtGui.QActionGroup(menu3)
                group3.triggered.connect(self.on_group3_triggered)
                for group in groups:
                    a = menu3.addAction(group[1])
                    a.bookid = bookid
                    a.groupid = group[0]
                    group3.addAction(a)
                menu.addMenu(menu3)
        return menu

    def on_group1_triggered(self, action):
        self.startProgramDetached(action.program, action.args)

    def on_group2_triggered(self, action):
        self.fetchAll()
        self._db.addBookToGroup(action.bookid, action.groupid)
        self.booksByGroupModel.refresh()

    def on_group3_triggered(self, action):
        self.fetchAll()
        self._db.removeBookFromGroup(action.bookid, action.groupid)
        for index in self.booksByGroupView.selectionModel().selectedRows():
            self.booksByGroupView.setRowHidden(index.row(), True)

    def on_booksByAuthorView_rightButtonPressed(self, index):
        model = self.booksByAuthorModel
        if index.isValid():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.makePopupMenu(bookid).exec_(QtGui.QCursor.pos())

    def on_booksBySeqView_rightButtonPressed(self, index):
        model = self.booksBySeqModel
        if index.isValid():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.makePopupMenu(bookid).exec_(QtGui.QCursor.pos())

    def on_booksByGenreView_rightButtonPressed(self, index):
        model = self.booksByGenreModel
        if index.isValid():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.makePopupMenu(bookid).exec_(QtGui.QCursor.pos())

    def on_bookSearchView_rightButtonPressed(self, index):
        model = self.bookSearchModel
        if index.isValid():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.makePopupMenu(bookid).exec_(QtGui.QCursor.pos())

    def on_booksByGroupView_rightButtonPressed(self, index):
        model = self.booksByGroupModel
        if index.isValid():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.makePopupMenu(bookid).exec_(QtGui.QCursor.pos())

    def on_authorsView_rightButtonPressed(self, index):
        model = self.authorsModel
        if index.isValid():
            authorid = model.record(index.row()).value(0).toInt()[0]
            menu = QtGui.QMenu()
            g = QtGui.QActionGroup(menu)
            g.triggered.connect(self.on_remove_author_action_triggered)
            a = menu.addAction(self.tr("Remove author"))
            a.authorid = authorid
            g.addAction(a)
            menu.exec_(QtGui.QCursor.pos())

    def on_sequencesView_rightButtonPressed(self, index):
        model = self.sequencesModel
        if index.isValid():
            seqid = model.record(index.row()).value(0).toInt()[0]
            menu = QtGui.QMenu()
            g = QtGui.QActionGroup(menu)
            g.triggered.connect(self.on_remove_sequence_action_triggered)
            a = menu.addAction(self.tr("Remove sequence"))
            a.seqid = seqid
            g.addAction(a)
            menu.exec_(QtGui.QCursor.pos())

    def on_groupsView_rightButtonPressed(self, index):
        model = self.groupsModel
        if index.isValid():
            groupid = model.record(index.row()).value(0).toInt()[0]
            menu = QtGui.QMenu()
            g = QtGui.QActionGroup(menu)
            g.triggered.connect(self.on_remove_group_action_triggered)
            a = menu.addAction(self.tr("Remove group"))
            a.groupid = groupid
            g.addAction(a)
            menu.exec_(QtGui.QCursor.pos())

    def on_remove_author_action_triggered(self, action):
        self.fetchAll()
        self._db.removeAuthor(action.authorid)
        for index in self.authorsView.selectionModel().selectedRows():
            self.authorsView.setRowHidden(index.row(), True)

    def on_remove_sequence_action_triggered(self, action):
        self.fetchAll()
        self._db.removeSequence(action.seqid)
        for index in self.sequencesView.selectionModel().selectedRows():
            self.sequencesView.setRowHidden(index.row(), True)

    def on_remove_group_action_triggered(self, action):
        self.fetchAll()
        self._db.removeGroup(action.groupid)
        for index in self.groupsView.selectionModel().selectedRows():
            self.groupsView.setRowHidden(index.row(), True)

    @QtCore.pyqtSlot()
    def on_actionAboutQt_triggered(self):
        QtGui.QMessageBox.aboutQt(self, self.tr("About Qt"))

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        msgbox = QtGui.QMessageBox(QtGui.QMessageBox.NoIcon,
                                   self.tr("About PyHomeLib"),
                                   QtCore.QString(self.tr("<b>Homepage</b>: %1"))
                                   .arg("<a href='http://github.com/md2/pyhomelib'>http://github.com/md2/pyhomelib</a>"),
                                   QtGui.QMessageBox.Ok,
                                   self)
        msgbox.exec_()

    def on_groupEdit_returnPressed(self):
        self.fetchAll()
        self._db.addGroup(self.groupEdit.text())
        self.groupsModel.refresh()
        self.groupEdit.clear()

    def on_searchByAuthorEdit_returnPressed(self):
        self.setSearchModelQuery()

    def on_searchByTitleEdit_returnPressed(self):
        self.setSearchModelQuery()

    def on_searchBySeqEdit_returnPressed(self):
        self.setSearchModelQuery()

    def on_searchByGenreEdit_returnPressed(self):
        self.setSearchModelQuery()

    def on_searchByFileAuthorEdit_returnPressed(self):
        self.setSearchModelQuery()

    def on_searchByMd5Edit_returnPressed(self):
        self.setSearchModelQuery()

    def setSearchModelQuery(self):
        model = self.bookSearchModel
        author = self.searchByAuthorEdit.text().trimmed()
        title = self.searchByTitleEdit.text().trimmed()
        seq = self.searchBySeqEdit.text().trimmed()
        genre = self.searchByGenreEdit.text().trimmed()
        fileauthor = self.searchByFileAuthorEdit.text().trimmed()
        md5 = self.searchByMd5Edit.text().trimmed()
        l = QtCore.QStringList()
        if not author.isEmpty():
            l.append("lastname LIKE ?")
            model.addBindValue(author.append('%'))
        if not title.isEmpty():
            l.append("title LIKE ?")
            model.addBindValue(title.append('%'))
        if not seq.isEmpty():
            l.append("seqname LIKE ?")
            model.addBindValue(seq.append('%'))
        if not genre.isEmpty():
            char = genre[0].toAscii()
            if char >= 'a' and char <= 'z':
                l.append("genrecode LIKE ?")
            else:
                l.append("genredesc LIKE ?")
            model.addBindValue(genre.append('%'))
        if not fileauthor.isEmpty():
            l.append("fileauthor LIKE ?")
            model.addBindValue(fileauthor.append('%'))
        if not md5.isEmpty():
            l.append("md5 = ?")
            model.addBindValue(md5.toLower().toAscii())
        sql = l.join(" AND ")
        if not sql.isEmpty():
            model.setWhereClause(sql)
            model.select()

    def fetchAll(self):
        for widget in self.findChildren(QtGui.QTableView):
            while widget.model().canFetchMore():
                widget.model().fetchMore()
                QtGui.qApp.processEvents()

    def on_booksByAuthorView_clicked(self, index):
        model = self.booksByAuthorModel
        if self.dockWidget.isVisible():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksBySeqView_clicked(self, index):
        model = self.booksBySeqModel
        if self.dockWidget.isVisible():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_bookSearchView_clicked(self, index):
        model = self.bookSearchModel
        if self.dockWidget.isVisible():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksByGenreView_clicked(self, index):
        model = self.booksByGenreModel
        if self.dockWidget.isVisible():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    def on_booksByGroupView_clicked(self, index):
        model = self.booksByGroupModel
        if self.dockWidget.isVisible():
            bookid = model.record(index.row()).value(0).toInt()[0]
            self.parserThread.parse(bookid)

    @QtCore.pyqtSlot()
    def on_actionStatistics_triggered(self):
        dlg = StatisticsDialog(self._db, self)
        dlg.exec_()

    def on_dockWidget_visibilityChanged(self, visible):
        self.actionViewBookInfo.setChecked(self.dockWidget.isVisibleTo(self))

    def on_quickFindShortcut_activated(self):
        self.tabWidget.setCurrentIndex(3)
        self.searchForWidget.show()

    def on_searchForWidget_returnPressed(self):
        self.quickFind()

    def quickFind(self):
        model = self.bookSearchModel
        text = self.searchForWidget.text().trimmed().append("%")
        sql = "lastname LIKE ? OR title LIKE ? OR seqname LIKE ?"
        for i in range(3):
            model.addBindValue(text)
        model.setWhereClause(sql)
        model.select()

