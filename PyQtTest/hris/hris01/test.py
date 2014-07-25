#!/usr/bin/python
'''
Created on Jul 22, 2014

@author: pandazen.wordpress.com
'''
import hrisdb, hriseditor
from PyQt5.QtWidgets import QApplication

def main():
  import sys
  
  app = QApplication(sys.argv)
  
  db = hrisdb.Database("D:\pyr.mdb","ItC802.g11")
  
  if not db.dbConnect():
    sys.exit(1)
    
  editor = hriseditor.TableEditor('tmp')
  editor.show()
  sys.exit(editor.exec_())
        
if __name__ == '__main__':
  main()        