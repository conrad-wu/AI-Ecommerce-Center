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
from modules.batch_processor import create_sample_excel, process_excel
from modules.product_library import get_product_by_name, get_product_names
from modules.asset_exporter import export_material_package

try:
    from modules.openai_generator import generate_ai_markdown
except Exception:
    generate_ai_markdown = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Ecommerce Center V8.6')
        self.resize(1220, 920)
        self.latest_markdown = ''

        root = QWidget()
        main_layout = QVBoxLayout(root)

        title = QLabel('AI Ecommerce Center V8.6 - Product Library, Listing, Batch Excel & Material Package Generator')
        title.setStyleSheet('font-size: 20px; font-weight: bold; margin-bottom: 8px;')
        main_layout.addWidget(title)

        form = QFormLayout()

        self.product_library = QComboBox()
        self.product_library.addItem('Custom / 自定义')
        self.product_library.addItems(get_product_names())

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

        library_row = QHBoxLayout()
        library_row.addWidget(self.product_library)
        load_btn = QPushButton('Load Product / 自动填充')
        load_btn.clicked.connect(self.load_product_from_library)
        library_row.addWidget(load_btn)

        form.addRow('Product Library / 产品库型号', library_row)
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
        package_btn = QPushButton('Export Material Package / 导出素材包')
        package_btn.clicked.connect(self.export_material_package_ui)
        clear_btn = QPushButton('Clear / 清空')
        clear_btn.clicked.connect(self.clear_output)

        button_layout.addWidget(generate_btn)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(package_btn)
        button_layout.addWidget(clear_btn)
        main_layout.addLayout(button_layout)

        batch_layout = QHBoxLayout()
        sample_btn = QPushButton('Create Excel Template / 创建Excel模板')
        sample_btn.clicked.connect(self.create_excel_template)
        batch_btn = QPushButton('Batch Generate Excel / 批量生成Excel')
        batch_btn.clicked.connect(self.batch_generate_excel)

        batch_layout.addWidget(sample_btn)
        batch_layout.addWidget(batch_btn)
        main_layout.addLayout(batch_layout)

        tips = QLabel('Tip: Material Package exports listing.md, image_prompts.txt and assets.json for design / PSD workflow.')
        tips.setStyleSheet('color: #666; margin: 4px 0;')
        main_layout.addWidget(tips)

        self.output = QTextEdit()
        self.output.setPlaceholderText('Generated Amazon / TEMU / TikTok / A+ content will appear here...')
        main_layout.addWidget(self.output)

        self.setCentralWidget(root)

    def load_product_from_library(self):
        name = self.product_library.currentText()
        if name.startswith('Custom'):
            QMessageBox.information(self, 'Product Library', 'Please select a product model from the library.')
            return

        product = get_product_by_name(name)
        if not product:
            QMessageBox.warning(self, 'Product Library', f'No data found for {name}.')
            return

        self.brand.setText(product.get('brand', ''))
        self.model.setText(product.get('model', ''))
        self.layout.setText(product.get('layout', ''))
        self.switch.setText(product.get('switch', ''))
        self.connection.setText(product.get('connection', ''))
        self.language.setText(product.get('language', ''))
        self.color.setText(product.get('color', ''))
        self.battery.setText(product.get('battery', ''))
        self.rgb.setText(product.get('rgb', ''))

        self.output.setPlainText(f'Loaded product from library: {name}\n\nYou can adjust color, platform or language before generating content.')

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

    def export_material_package_ui(self):
        product = self.collect_product()
        root_dir = QFileDialog.getExistingDirectory(self, 'Select Material Package Output Folder')
        if not root_dir:
            return

        try:
            output_dir = export_material_package(product, root_dir)
            QMessageBox.information(self, 'Material Package Exported', f'Material package saved:\n{os.path.abspath(output_dir)}')
            self.output.setPlainText(
                f'Material package exported successfully.\n\nFolder:\n{output_dir}\n\nFiles:\n- listing.md\n- image_prompts.txt\n- assets.json'
            )
        except Exception as error:
            QMessageBox.critical(self, 'Material Package Export Failed', str(error))

    def create_excel_template(self):
        default_name = 'AI_Ecommerce_Batch_Template.xlsx'
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save Excel Template',
            default_name,
            'Excel Files (*.xlsx)'
        )
        if not path:
            return

        try:
            create_sample_excel(path)
            QMessageBox.information(self, 'Template Created', f'Excel template saved:\n{os.path.abspath(path)}')
        except Exception as error:
            QMessageBox.critical(self, 'Create Template Failed', str(error))

    def batch_generate_excel(self):
        input_file, _ = QFileDialog.getOpenFileName(
            self,
            'Select Input Excel',
            '',
            'Excel Files (*.xlsx *.xls)'
        )
        if not input_file:
            return

        default_output = f"AI_Ecommerce_Batch_Output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            'Save Output Excel',
            default_output,
            'Excel Files (*.xlsx)'
        )
        if not output_file:
            return

        try:
            process_excel(input_file, output_file)
            QMessageBox.information(self, 'Batch Complete', f'Batch output saved:\n{os.path.abspath(output_file)}')
            self.output.setPlainText(f'Batch generation completed.\n\nInput:\n{input_file}\n\nOutput:\n{output_file}')
        except Exception as error:
            QMessageBox.critical(self, 'Batch Generate Failed', str(error))

    def clear_output(self):
        self.output.clear()
        self.latest_markdown = ''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
