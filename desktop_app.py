from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QLabel,QLineEdit,QPushButton,QTextEdit
from modules.content_generator import generate_amazon_title,generate_bullets
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Ecommerce Center')
        self.resize(900,700)

        widget=QWidget()
        layout=QVBoxLayout(widget)

        self.brand=QLineEdit('AJAZZ')
        self.model=QLineEdit('AK820 MAX')

        layout.addWidget(QLabel('Brand'))
        layout.addWidget(self.brand)
        layout.addWidget(QLabel('Model'))
        layout.addWidget(self.model)

        btn=QPushButton('Generate Content')
        btn.clicked.connect(self.generate)
        layout.addWidget(btn)

        self.output=QTextEdit()
        layout.addWidget(self.output)

        self.setCentralWidget(widget)

    def generate(self):
        product={
            'brand':self.brand.text(),
            'model':self.model.text(),
            'switch':'Magnetic Switch',
            'layout':'75%',
            'connection':'Wired'
        }

        title=generate_amazon_title(product)
        bullets='\n'.join(generate_bullets(product))

        self.output.setPlainText(f'Amazon Title:\n{title}\n\nBullets:\n{bullets}')

app=QApplication(sys.argv)
window=MainWindow()
window.show()
sys.exit(app.exec())
