#!/usr/bin/python
'''
Created on Jul 22, 2014

@author: pandazen.wordpress.com
'''

from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog

class Database:
  def __init__(self,sDBF,sPW):
    self.sDBF = sDBF
    self.sPW = sPW
    
  def checkFile(self,sFileName):
    import os
    
    if not (os.path.isfile(sFileName) and os.access(sFileName, os.R_OK)):
      QMessageBox.information(None,"Check file","Either file is missing or is not readable")
      qFileName = QFileDialog.getOpenFileName(None, 'Open File', '.', '*.mdb')
      sFileName = qFileName[0]
        
      if not (os.path.isfile(sFileName) and os.access(sFileName, os.R_OK)):
        return False
      else:
        self.sDBF = sFileName
        return True
    else:
      return True    
    
  def dbConnect(self):
    if self.checkFile(self.sDBF):
      sConnection = "DRIVER={Microsoft Access Driver (*.mdb)};DBQ={MS Access};DBQ="+self.sDBF+";PWD="+self.sPW
      self.db = QSqlDatabase.addDatabase("QODBC")
      self.db.setDatabaseName(sConnection)  
      print(sConnection)              
    
      if not self.db.open():
        #catch db error
        if self.db.lastError().number() == 0:
          sErrMsg = "There is no error occured"
        elif self.db.lastError().number() == 1:
          sErrMsg = "Connection error"
        elif self.db.lastError().number() == 2:
          sErrMsg = "SQL statement syntax error"
        elif self.db.lastError().number() == 3:
          sErrMsg = "Transaction failed error"
        elif self.db.lastError().number() == 4:
          sErrMsg = "Unknown error"
        else:
          sErrMsg = "Unable to establish a database connection.\n" \
                  "This example needs database support. Please read the Qt SQL " \
                  "driver documentation for information how to build it.\n\n" \
                  "Click Cancel to exit."
                  
        QMessageBox.critical(None, "Open database",sErrMsg + ' ' + str(self.db.lastError().text()),QMessageBox.Cancel)
        return False
        #catch db error, return False
      #no db error, return True
      return True
    
      #self.db.open()
      #print(self.db.lastError().text())
    


# Main must be outside the table class
#def main():
#  db = Database("D:\pysr.mdb","ItC802.g11")
#  
#  if not db.dbConnect():
#        sys.exit(1)
#        
#if __name__ == '__main__':
#  import sys
#  app = QApplication(sys.argv)
#  main()        
        
