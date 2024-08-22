from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QMessageBox
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize
from math import pi, sqrt, cbrt
import sys


class Button(QPushButton):
    def __init__(self, parent, name, image, x, y):
        super().__init__(parent)

        self.name = name
        self.parent = parent
        self.setIcon(QIcon(image))
        self.setIconSize(QSize(100, 100))
        self.setFixedSize(100, 100)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("border: 0px")
        self.move(x, y)
        self.clicked.connect(self.func())


    def func(self):
        if self.name == "=":
            return self.calc
        elif self.name == "c":
            return self.reset_calc
        else:
            return self.add_order

        
    def reset_calc(self):
        self.parent.order = ""
        self.parent.txt_edit.setText(self.parent.order)

    
    def add_order(self):
        orders = ["+", "-", "*", "/"]
        string = self.parent.order
        if self.name == "<":
            self.parent.order = self.parent.order[:-1]
        elif len(string) != 0 and string[-1] in orders and self.name in orders:
            self.parent.order = self.parent.order[0:-1] + self.name
        elif len(string) != 0 and self.name in ["(", "sqrt(", "cbrt("] and (string[-1].isnumeric() or string[-1] == ")"):
            self.parent.order += "*" + self.name
        # If we cannot hit (.), the condition is executed and does nothing,
        # otherwise, the else condition is executed and (.) is added.
        elif self.name == "." and self.check_dot():
            pass
        else:
            self.parent.order += self.name
        self.parent.txt_edit.setText(self.parent.order)

    
    def check_dot(self):
        for char in self.parent.order[::-1]:
            if char in [".", ")"]:
                return True
            elif char in ["+", "-", "*", "/", "**"]:
                break
        return False


    def calc(self):
        try:
            result = eval(self.parent.order)
        except SyntaxError:
            self.show_error("Invalid format")
        except ZeroDivisionError:
            self.show_error("Division by zero is not possible")
        else:
            if result == int(result):
                self.parent.order = str(int(result))
            else:
                self.parent.order = str(result)
            self.parent.txt_edit.setText(self.parent.order)


    def show_error(self, text):
        error = QMessageBox(QMessageBox.Icon.Critical, "Error", text, parent=self)
        error.setStyleSheet("color: black")
        error.show()
        self.reset_calc()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.order = ""

        self.setWindowTitle("Calculator")
        self.setWindowIcon(QIcon("images/title_icon.png"))
        self.setFixedSize(600, 730)
        self.setStyleSheet("background-color:#ffffff")

        # create calculator buttons
        self.btn_cbrt = Button(self, "cbrt(", "images/cbrt.png", 50, 600)
        self.btn_pi = Button(self, str(pi), "images/pi.png", 150, 600)
        self.btn_0 = Button(self, "0", "images/0.png", 250, 600)
        self.btn_dot = Button(self, ".", "images/dot.png", 350, 600)
        self.btn_result = Button(self, "=", "images/result.png", 450, 600)
        self.btn_sqrt = Button(self, "sqrt(", "images/sqrt.png", 50, 500)
        self.btn_1 = Button(self, "1", "images/1.png", 150, 500)
        self.btn_2 = Button(self, "2", "images/2.png", 250, 500)
        self.btn_3 = Button(self, "3", "images/3.png", 350, 500)
        self.btn_plus = Button(self, "+", "images/plus.png", 450, 500)
        self.btn_pown = Button(self, "**(", "images/pown.png", 50, 400)
        self.btn_4 = Button(self, "4", "images/4.png", 150, 400)
        self.btn_5 = Button(self, "5", "images/5.png", 250, 400)
        self.btn_6 = Button(self, "6", "images/6.png", 350, 400)
        self.btn_minus = Button(self, "-", "images/minus.png", 450, 400)
        self.btn_pow2 = Button(self, "**(2)", "images/pow2.png", 50, 300)
        self.btn_7 = Button(self, "7", "images/7.png", 150, 300)
        self.btn_8 = Button(self, "8", "images/8.png", 250, 300)
        self.btn_9 = Button(self, "9", "images/9.png", 350, 300)
        self.btn_multi = Button(self, "*", "images/multiplication.png", 450, 300)
        self.btn_c = Button(self, "c", "images/c.png", 50, 200)
        self.btn_parentheses1 = Button(self, "(", "images/(.png", 150, 200)
        self.btn_parentheses2 = Button(self, ")", "images/).png", 250, 200)
        self.btn_division = Button(self, "/", "images/division.png", 350, 200)
        self.btn_backspace = Button(self, "<", "images/backspace.png", 450, 200)

        self.txt_edit = QTextEdit(self)
        self.txt_edit.setFixedSize(500, 150)
        self.txt_edit.setFont(QFont("arial", 15))
        self.txt_edit.setStyleSheet("border: 4px solid black; color: black")
        self.txt_edit.move(50, 35)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    root = Window()
    root.show()

    sys.exit(app.exec())