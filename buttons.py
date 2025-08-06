import sqlite3
from typing import TYPE_CHECKING
from PySide6.QtWidgets import QPushButton,QGridLayout, QWidget
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
# from display import Display
from utils import isValidNumber
import math
from db_sqlite import insertToMemory
if TYPE_CHECKING:
    from display import Display
    from info    import Info
    from main_window import MainWindow


class Button(QPushButton):
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)

        self.configStyle()


    #Define o Stylo do Botão 
    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)

class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info : 'Info', window:'MainWindow', *args,**kwargs
                 ) -> None:
        super().__init__(*args,**kwargs)

        self._gridMask = [
            ['C', '◀', '^' ,'/'],
            ['7', '8', '9', '*' ],
            ['4', '5', '6', '-' ],
            ['1', '2', '3', '+' ],
            ['N',  '0', '.', '=' ],
        ]   

        self.display = display
        self.info = info
        self.window = window
        
        self._equation = ''
        self._equationInitialValue = 'Sua conta'
        self._right = None
        self._left = None
        self._op = None
        
        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)


    

    def _makeGrid(self):
        self.display.eqPressed.connect(
            self._eq,)#type:ignore
        
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)



        for i, row in enumerate(self._gridMask):
           for j, buttonText in enumerate(row):
                button = Button(buttonText)
                
                if buttonText not in '0123456789.':
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)
                           
                self.addWidget(button, i, j)
                slot = self._makeSlot( self._insertToDisplay, buttonText,)
                self._connectButtonClicked(button,slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot():
            func( *args, **kwargs)
        return realSlot
    
    def _configSpecialButton(self,button):
        text = button.text()
        
        if text =='C':
            # slot = self._makeSlot(self.display.clear)
            self._connectButtonClicked(button, self._clear)
        
        if text == '◀':  
           self._connectButtonClicked(button, self._backspace)                         
        
        if text == 'N':  
           self._connectButtonClicked(button, self.invertNumber)                         

        if text in '+-*/^':  
            self._connectButtonClicked(
                button, 
                self._makeSlot(self._configLeftOp, text))
        
        if text == '=':  
            self._connectButtonClicked(button, self._eq)

    @Slot()
    def _insertToDisplay(self,text):
        newDisplayValaue = self.display.text() + text

        if not isValidNumber(newDisplayValaue):
            return
        
        self.display.insert(text)
        self.display.setFocus()    
    @Slot()
    def invertNumber(self):
        displayText = self.display.text()
        if not isValidNumber(displayText):
            return

        newNumber= -float(displayText)
        self.display.setText(str(newNumber))

    @Slot()
    def _clear(self):
        self._right = None
        self._left = None
        self._op = None
        self.equation = self._equationInitialValue

        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text() #Deverá ser o numero _left
        self.display.clear() # Limpa o display 


        # Se a pessoa clicopi no operador sem configuar numero antes 
        if not isValidNumber(displayText) and self._left == None:
            self._showError('Você não digitou nada.')
            return  
        
        # Se houver algo no nùmero da esquerda, 
        # Não fazemos nada. Aguardaremos o número da direita. 
        if self._left is None:
            self._left = float(displayText)
            
        self._op = text
        self.equation = f'{self._left}{self._op} ??'
        self.display.setFocus()    
    @Slot()
    def _eq(self):
        displayText = self.display.text()
        
        if not isValidNumber(displayText) or self._left is None:
            self._showError('Conta incompleta.')
            return 
        
        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 0.0
        
        

        try:
            if '^' in self.equation and isinstance( self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)

        except ZeroDivisionError:
            self._showError('Divisão por zero')
        
        except OverflowError:
            self._showError( 'ERROR: Numero muito grande')
        
        
        
        insertToMemory(self._left, self._right, self._op, result) #type: ignore
        
        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')    
        self._left = result
        self._right = None
        if result == 'ERROR: Numero muito grande':
            self._left = None
        self.display.setFocus()
        

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox
    
    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()
    
    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()

   