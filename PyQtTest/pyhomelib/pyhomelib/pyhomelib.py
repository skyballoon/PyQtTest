#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5 import QtCore, QtWidgets, QtGui, QtSql


def init():
    try:
        import pyhomelib
        sys.path.append(os.path.dirname(pyhomelib.__file__))
    except ImportError:
        pass


def main():
    init()

    app = QtWidgets.QApplication(sys.argv)

    from mainwindow import MainWindow
    if not QtSql.QSqlDatabase.drivers().contains("QSQLITE"):
        raise (Exception, "Fatal error: QSQLITE database driver is not found!")

    qttranslator = QtCore.QTranslator()
    if qttranslator.load("qt_" + QtCore.QLocale.system().name(),
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)):
        app.installTranslator(qttranslator)

    translator = QtCore.QTranslator()
    if translator.load("pyhomelib_" + QtCore.QLocale.system().name()):
        app.installTranslator(translator)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
