'''
Created on Jun 27, 2014

@author: wi
'''

from PyQt5 import QtWidgets, QtSql
 
import sys

def main():
      
    app     = QtWidgets.QApplication(sys.argv)
    table   = QtWidgets.QTableWidget()
    db      = QtSql.QSqlDatabase.addDatabase("QOCI")  
 
    if ((QtSql.QSqlDatabase.isDriverAvailable("QOCI"))==False):
        QtWidgets.QMessageBox.critical(None, "Driver Not Available", db.lastError().text())
        
       
    table.setWindowTitle("Connect to Oracle Database Example")   
    
    db.setHostName("192.168.51.55")
    db.setDatabaseName("itcapps2")
    db.setUserName("wi")
    db.setPassword("W1J35500.23")
    
    if (db.open()==False):     
        QtWidgets.QMessageBox.critical(None, "Database Error", db.lastError().text())   
    
    sSQL = "SELECT * FROM MIS.BADLOG where data='CR20214010070'"            
    query = QtSql.QSqlQuery ()
    query.setForwardOnly(True)  
    query.exec(sSQL)
    
    print(query.isForwardOnly())
    
    print(query.record().count())
    print(query.isActive())
    print(query.size())
    table.setColumnCount(query.record().count())
    #table.setRowCount(query.size())
    table.setRowCount(5)
    
    index=0
    while (query.next()):        
        table.setItem(index,0,QtWidgets.QTableWidgetItem(query.value(0)))
        
        index = index+1
    
    table.show()
    
    return app.exec_()

if __name__ == '__main__':
    main()