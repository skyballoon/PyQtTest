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
    
    db.setHostName("192.168.51.10")
    db.setDatabaseName("testsvr")
    db.setUserName("wi")
    db.setPassword("J3557yn00")
    
    if (db.open()==False):     
        QtWidgets.QMessageBox.critical(None, "Database Error", db.lastError().text())   
                
    query = QtSql.QSqlQuery ("SELECT * FROM mis.badlog")   
    
    print(query.record().count())
    print(query.size())
    table.setColumnCount(query.record().count())
    table.setRowCount(query.size())
    
    index=0
    while (query.next()):
        table.setItem(index,0,QtWidgets.QTableWidgetItem(query.value(0)))
        table.setItem(index,1,QtWidgets.QTableWidgetItem(str(query.value(1))))
        index = index+1
    
    table.show()
    
    return app.exec_()

if __name__ == '__main__':
    main()