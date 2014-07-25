'''
Created on Jun 27, 2014

@author: wi
'''

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets  import QTableWidget,QApplication,QMessageBox
import sys

#Define MyTableWidget Class Here ---------------
class MyTableWidget(QTableWidget):  
  def __init__(self):
    QTableWidget.__init__(self)
    self.setWindowTitle("QTableWidget Cell Click")
    self.setRowCount(1)
    self.setColumnCount(2)
        
##-----------------------------------------    
  @pyqtSlot(int,int)
  def slotItemClicked(self,item,item2):
    QMessageBox.information(self,
                "QTableWidget Cell Click",
                "Row: "+ str(item)+" |Column: "+str(item2))
#End of MyTableWidget Class Definition ---------------
 


def main():
  app = QApplication(sys.argv)
  window = MyTableWidget()
  window.cellClicked.connect(window.slotItemClicked)
  window.show() 
  return app.exec_()
 
if __name__ == '__main__': 
  main() 