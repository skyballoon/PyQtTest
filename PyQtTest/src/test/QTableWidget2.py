'''
Created on Jun 27, 2014

@author: wi
'''

from PyQt5.QtCore import pyqtSlot,pyqtSignal,Qt
from PyQt5.QtWidgets import QTableWidget,QApplication,QPushButton,QVBoxLayout,QTableWidgetItem,QMessageBox
import sys

#Define MainWindow Class Here ---------------
class MainWindow(QTableWidget):
  updateSignal = pyqtSignal()
  def __init__(self, parent=None):
    super(MainWindow, self).__init__(parent)
    self.table_widget = QTableWidget()
    self.button = QPushButton('Populate')
    self.button.clicked.connect(self.populate)
    layout = QVBoxLayout()
    layout.addWidget(self.table_widget)
    layout.addWidget(self.button)
    self.setLayout(layout)
    self.updateSignal.connect(self.update_table)
    self.updateSignal.connect(self.slotItemClicked(self,item,item2))
    self.populate()

##-----------------------------------------    
  @pyqtSlot(int,int)
  def slotItemClicked(self,item,item2):
    QMessageBox.information(self,
                "QTableWidget Cell Click",
                "Row: "+ str(item)+" |Column: "+str(item2))    

  def populate(self):
    ncols, nrows = 2,5
    self.setWindowTitle("QTableWidget Cell Click")
    self.table_widget.setSortingEnabled(False)
    self.table_widget.setRowCount(nrows)
    self.table_widget.setColumnCount(ncols)
    for i in range(nrows):
      for j in range(ncols):
        item = QTableWidgetItem('%s%s' % (i, j))
        self.table_widget.setItem(i, j, item)
        self.updateSignal.emit()
        self.table_widget.setSortingEnabled(True)

  def update_table(self):
    self.table_widget.sortItems(1,Qt.DescendingOrder)


#End of MainWindow Class Definition ---------------    

def main():
  app = QApplication(sys.argv)
  wnd = MainWindow()
  wnd.cellClicked.connect(wnd.slotItemClicked)
  wnd.resize(640, 480)
  wnd.show()
  sys.exit(app.exec_())
  #return app.exec_()

if __name__ == "__main__":
  main()