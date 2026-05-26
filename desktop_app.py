import os
import sys
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from modules.content_generator import generate_markdown

try:
    from modules.openai_generator import generate_ai_markdown
except Exception:
    generate_ai_markdown = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Ecommerce Center V5')
        self.resize(1150, 850)
        self.latest_markdown = ''

        root = QWidget()
        main_layout = QVBoxLayout(root)

        title = QLabel('AI Ecommerce Center V5 - Listing & Material Generator')
        title.setStyleSheet('font-size: 20px; font-weight: bold; margin-bottom: 8px;')
        main_layout.addWidget(title)

        form = QFormLayout()

        self.brand = QLineEdit('AJAZZ')
        self.model = QLineEdit('AK820 MAX')
        self.layout = QLineEdit('75%')
        self.switch = QLineEdit('Magnetic Switch')
        self.connection = QLineEdit('Wired')
        self.language = QLineEdit('German QWERTZ')
        self.color = QLineEdit('Grey White Yellow')
        self.battery = QLineEdit('8000mAh')
        self.rgb = QLineEdit('RGB')

        self.platform = QComboBox()
        self.platform.addItems(['Amazon', 'TEMU', 'TikTok Shop', 'AliExpress', 'All Platforms'])

        self.generate_mode = QComboBox()
        self.generate_mode.addItems(['Local Template / 本地模板', 'OpenAI AI / AI生成'])

        form.addRow('Brand / 品牌', self.brand)
        form.addRow('Model / 型号', self.model)
        form.addRow('Layout / 布局', self.layout)
        form.addRow('Switch / 轴体', self.switch)
        form.addRow('Connection / 连接方式', self.connection)
        form.addRow('Language Layout / 语言布局', self.language)
        form.addRow('Color / 配色', self.color)
        form.addRow('Battery / 电池', self.battery)
        form.addRow('Lighting / 灯光', self.rgb)
        form.addRow('Platform / 平台', self.platform)
        form.addRow('Generate Mode / 生成模式', self.generate_mode)

        main_layout.addLayout(form)

        button_layout = QHBoxLayout()
        generate_btn = QPushButton('Generate / 生成素材')
        generate_btn.clicked.connect(self.generate)
        export_btn = QPushButton('Export Markdown / 导出 Markdown')
        export_btn.clicked.connect(self.export_markdown)
        clear_btn = QPushButton('Clear / 清空')
        clear_btn.clicked.connect(self.clear_output)

        button_layout.addWidget(generate_btn)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(clear_btn)
        main_layout.addLayout(button_layout)

        tips = QLabel('Tip: OpenAI AI mode requires a .env file with OPENAI_API_KEY. Local Template mode works offline.')
        tips.setStyleSheet('color: #666; margin: 4px 0;')
        main_layout.addWidget(tips)

        self.output = QTextEdit()
        self.output.setPlaceholderText('Generated Amazon / TEMU / TikTok / A+ content will appear here...')
        main_layout.addWidget(self.output)

        self.setCentralWidget(root)

    def collect_product(self) -> dict:
        return {
            'brand': self.brand.text(),
            'model': self.model.text(),
            'layout': self.layout.text(),
            'switch': self.switch.text(),
            'connection': self.connection.text(),
            'language': self.language.text(),
            'color': self.color.text(),
            'battery': self.battery.text(),
            'rgb': self.rgb.text(),
            'platform': self.platform.currentText(),
        }

    def generate(self):
        product = self.collect_product()
        mode = self.generate_mode.currentText()

        try:
            if mode.startswith('OpenAI'):
                if generate_ai_markdown is None:
                    raise RuntimeError('OpenAI module is not available. Please check modules/openai_generator.py.')
                self.latest_markdown = generate_ai_markdown(product)
            else:
                self.latest_markdown = generate_markdown(product)

            self.output.setPlainText(self.latest_markdown)
        except Exception as error:
            QMessageBox.warning(
                self,
                'Generate Failed',
                f'{error}\n\nThe app will use Local Template mode instead.'
            )
            self.latest_markdown = generate_markdown(product)
            self.output.setPlainText(self.latest_markdown)

    def export_markdown(self):
        if not self.latest_markdown:
            self.generate()

        default_name = f"AI_Ecommerce_Output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save Markdown File',
            default_name,
            'Markdown Files (*.md);;Text Files (*.txt)'
        )

        if not path:
            return

        with open(path, 'w', encoding='utf-8') as file:
            file.write(self.latest_markdown)

        QMessageBox.information(self, 'Export Success', f'File saved:\n{os.path.abspath(path)}')

    def clear_output(self):
        self.output.clear()
        self.latest_markdown = ''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
