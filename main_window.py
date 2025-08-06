from PySide6.QtWidgets import  (QMainWindow, QWidget, QVBoxLayout,QMessageBox,)
from PySide6.QtGui import QAction
from db_sqlite import DB_FILE, cursor
import sqlite3
import os
import sys
# from PySide6.QtGui import QIcon

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS #type: ignore
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget |None = None, *args,**kwargs):
        
        super().__init__(parent, *args,**kwargs)
        


        # Configurando o layout básico 
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)
        
        # colocando titulo 
        self.setWindowTitle('Calculadora')
        
        self.createMenu()



     #  Última coisa a ser feita 
     # Define o tamanho do widget
    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(),self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)
        
    def makeMsgBox(self):
        return QMessageBox(self)
    
    def createMenu(self):
        
        menuBar = self.menuBar()
        
        #cria o menu historico
        historicoMenu = menuBar.addMenu('Historico')
        
        #cria uma ação (opção clicavel)
        showHistoricoAction = QAction('Ver historico', self)
        showHistoricoAction.triggered.connect(self._showMemory) #conecta ao slot
        
        #Adiciona a ação ao menu 
        historicoMenu.addAction(showHistoricoAction)


    def _showMemory(self):

        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        cursor.execute(
            'SELECT numberLeft, operator, numberRigth, '
            'result FROM Memory ORDER BY id DESC LIMIT 10 '
        )   
        rows = cursor.fetchall()

        if rows:
            history_text = ''
            for linha in rows:
                left, op, rigth, res = linha # pega os 4 valores da operação
                history_text += f'{left} {op} {rigth} = {res}\n'
        else:
            history_text ='Nenhuma operação registrada ainda.'

        connection.commit()
        msgbox = self.makeMsgBox()
        msgbox.setWindowTitle('Historico')
        msgbox.setText(history_text)
        # msgbox.setIcon(msgbox.Icon.Information)
        msgbox.exec()
        
        cursor.close()
        connection.close()
