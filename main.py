from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit)
from display import Display
from main_window import MainWindow
from variables import WINDOW_ICON_PATH
from info import Info
import styles
import sys

from buttons import Button, ButtonsGrid


if __name__ == '__main__':
    # snake_case (metodos / variaveis )
    # PascalCase (Classes)
    # camelCase


    # cria a aplicação 
    app = QApplication(sys.argv)
    styles.setupTheme(app)
    window = MainWindow()
    
 
    # Define o Icone 
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)  
    # app.setWindowIcon(icon)
    app.setWindowIcon(QIcon(str(WINDOW_ICON_PATH)))

    # label1 = QLabel('Texto')
    # # label1.setStyleSheet('font-size: 50px;')
    # window.addToVLayout(label1)
    # window.adjustFixedSize()
    
    # info 
    info = Info()
    window.addWidgetToVLayout(info) 
   
    
    # Display
    display = Display()
    window.addWidgetToVLayout(display)
    display.setPlaceholderText('')
    
    # Grid 
    buttunsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttunsGrid)
    button = Button('Texto do botão')



    # Button 
    # button = Button('Botão 1 ')
    # window.addWidgetToVLayout(button)
    # # button.set

    # fixa o tamanho da widget
    window.adjustFixedSize()
    
    # executa tudo 
    window.show()
    app.exec()
    