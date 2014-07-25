#!/usr/bin/python
'''
Created on Jul 21, 2014

@author: pandazen.wordpress.com
'''

from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtSql import QSqlDatabase
import os



def checkFile(sFilename):
  if not (os.path.isfile(sFilename) and os.access(sFilename, os.R_OK)):
    QMessageBox.information(None,"Check file","Either file is missing or is not readable")
    sFilename = QFileDialog.getOpenFileName()
      
    if not (os.path.isfile(sFilename) and os.access(sFilename, os.R_OK)):
      return False
    else:
      return True
  else:
    return True

def createConnection(): 
  sFilename = "D:\pyrs.mdb"     
  if checkFile(sFilename):    
    #begin-if file exists then open db
    #save to log-QMessageBox.information(None, "Check file", "File exists and is readable")
  
    sPassword = "ItC802.g11" 
    sConnection = "DRIVER={Microsoft Access Driver (*.mdb)};DBQ={MS Access};DBQ="+sFilename+";PWD="+sPassword
    db = QSqlDatabase.addDatabase('QODBC')    
    db.setDatabaseName(sConnection)
    
    if not db.open():
      #catch db error
      if db.lastError().number() == 0:
        sErrMsg = "There is no error occured"
      elif db.lastError().number() == 1:
        sErrMsg = "Connection error"
      elif db.lastError().number() == 2:
        sErrMsg = "SQL statement syntax error"
      elif db.lastError().number() == 3:
        sErrMsg = "Transaction failed error"
      elif db.lastError().number() == 4:
        sErrMsg = "Unknown error"
      else:
        sErrMsg = "Unable to establish a database connection.\n" \
                "This example needs database support. Please read the Qt SQL " \
                "driver documentation for information how to build it.\n\n" \
                "Click Cancel to exit."
                
      QMessageBox.critical(None, "Open database",sErrMsg + ' ' + str(db.lastError().text()),QMessageBox.Cancel)
      return False
      #end catch db error  
    #end if file exists        
  #end file exists
  return True
