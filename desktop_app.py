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
from modules.product_database import upsert_product, search_products, find_product_by_sku
from modules.product_importer import create_product_import_template, import_products_from_excel

try:
    from modules.openai_generator import generate_ai_markdown
except Exception:
    generate_ai_markdown = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Ecommerce Center V10.2')
        self.resize(1260, 960)
        self.latest_markdown = ''

        root = QWidget()
        main_layout = QVBoxLayout(root)

        title = QLabel('AI Ecommerce Center V10.2 - Product Center, Import, Listing, Batch & Material Package')
        title.setStyleSheet('font-size: 20px; font-weight: bold; margin-bottom: 8px;')
        main_layout.addWidget(title)

        form = QFormLayout()

        self.product_library = QComboBox()
        self.product_library.addItem('Custom / 自定义')
        self.product_library.addItems(get_product_names())

        self.sku = QLineEdit('AK820MAX-DE-GWY')
        self.brand = QLineEdit('AJAZZ')
        self.model = QLineEdit('AK820 MAX')
        self.category = QLineEdit('Keyboard')
        self.layout = QLineEdit('75%')
        self.switch = QLineEdit('Magnetic Switch')
        self.connection = QLineEdit('Wired')
        self.language = QLineEdit('German QWERTZ')
        self.color = QLineEdit('Grey White Yellow')
        self.battery = QLineEdit('8000mAh')
        self.rgb = QLineEdit('RGB')
        self.weight = QLineEdit('')
        self.dimensions = QLineEdit('')
        self.notes = QLineEdit('')

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
        form.addRow('SKU', self.sku)
        form.addRow('Brand / 品牌', self.brand)
        form.addRow('Model / 型号', self.model)
        form.addRow('Category / 分类', self.category)
        form.addRow('Layout / 布局', self.layout)
        form.addRow('Switch / 轴体', self.switch)
        form.addRow('Connection / 连接方式', self.connection)
        form.addRow('Language Layout / 语言布局', self.language)
        form.addRow('Color / 配色', self.color)
        form.addRow('Battery / 电池', self.battery)
        form.addRow('Lighting / 灯光', self.rgb)
        form.addRow('Weight / 重量', self.weight)
        form.addRow('Dimensions / 尺寸', self.dimensions)
        form.addRow('Platform / 平台', self.platform)
        form.addRow('Notes / 备注', self.notes)
        form.addRow('Generate Mode / 生成模式', self.generate_mode)

        main_layout.addLayout(form)

        db_layout = QHBoxLayout()
        save_db_btn = QPushButton('Save to DB / 保存到数据库')
        save_db_btn.clicked.connect(self.save_product_to_db)
        load_db_btn = QPushButton('Load by SKU / 按SKU加载')
        load_db_btn.clicked.connect(self.load_product_by_sku)
        search_db_btn = QPushButton('Search DB / 搜索数据库')
        search_db_btn.clicked.connect(self.search_product_db)
        create_import_template_btn = QPushButton('Create Product Import Template / 产品导入模板')
        create_import_template_btn.clicked.connect(self.create_product_import_template_ui)
        import_products_btn = QPushButton('Import Products to DB / 导入产品库')
        import_products_btn.clicked.connect(self.import_products_to_db_ui)

        db_layout.addWidget(save_db_btn)
        db_layout.addWidget(load_db_btn)
        db_layout.addWidget(search_db_btn)
        db_layout.addWidget(create_import_template_btn)
        db_layout.addWidget(import_products_btn)
        main_layout.addLayout(db_layout)

        button_layout = QHBoxLayout()
        generate_btn = QPushButton('Generate / 生成素材')
        generate_btn.clicked.connect(self.generate)
        export_btn = QPushButton('Export Markdown / 导出 Markdown')
        export_btn.clicked.connect(self.export_markdown)
        package_btn = QPushButton('Generate Package / 一键素材包')
        package_btn.clicked.connect(self.export_material_package_ui)
        clear_btn = QPushButton('Clear / 清空')
        clear_btn.clicked.connect(self.clear_output)

        button_layout.addWidget(generate_btn)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(package_btn)
        button_layout.addWidget(clear_btn)
        main_layout.addLayout(button_layout)

        batch_layout = QHBoxLayout()
        sample_btn = QPushButton('Create Listing Excel Template / Listing模板')
        sample_btn.clicked.connect(self.create_excel_template)
        batch_btn = QPushButton('Batch Generate Listing Excel / 批量Listing')
        batch_btn.clicked.connect(self.batch_generate_excel)

        batch_layout.addWidget(sample_btn)
        batch_layout.addWidget(batch_btn)
        main_layout.addLayout(batch_layout)

        tips = QLabel('Tip: V10.2 supports Excel → Product DB, single-product package generation, and batch listing export.')
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
        self.category.setText('Keyboard' if product.get('layout', '') != 'Mouse' else 'Mouse')
        self.sku.setText(f"{product.get('brand', '')}-{product.get('model', '')}".replace(' ', '_'))

        self.output.setPlainText(f'Loaded product from library: {name}\n\nYou can adjust SKU, color, platform or language before saving / generating content.')

    def collect_product(self) -> dict:
        return {
            'sku': self.sku.text(),
            'brand': self.brand.text(),
            'model': self.model.text(),
            'category': self.category.text(),
            'layout': self.layout.text(),
            'switch': self.switch.text(),
            'connection': self.connection.text(),
            'language': self.language.text(),
            'color': self.color.text(),
            'battery': self.battery.text(),
            'rgb': self.rgb.text(),
            'weight': self.weight.text(),
            'dimensions': self.dimensions.text(),
            'platform': self.platform.currentText(),
            'notes': self.notes.text(),
        }

    def fill_product_form(self, product: dict):
        self.sku.setText(product.get('sku', ''))
        self.brand.setText(product.get('brand', ''))
        self.model.setText(product.get('model', ''))
        self.category.setText(product.get('category', ''))
        self.layout.setText(product.get('layout', ''))
        self.switch.setText(product.get('switch', ''))
        self.connection.setText(product.get('connection', ''))
        self.language.setText(product.get('language', ''))
        self.color.setText(product.get('color', ''))
        self.battery.setText(product.get('battery', ''))
        self.rgb.setText(product.get('rgb', ''))
        self.weight.setText(product.get('weight', ''))
        self.dimensions.setText(product.get('dimensions', ''))
        self.notes.setText(product.get('notes', ''))

    def save_product_to_db(self):
        try:
            sku = upsert_product(self.collect_product())
            QMessageBox.information(self, 'Product Saved', f'Product saved to database:\n{sku}')
            self.output.setPlainText(f'Product saved to database: {sku}')
        except Exception as error:
            QMessageBox.critical(self, 'Save Failed', str(error))

    def load_product_by_sku(self):
        sku = self.sku.text().strip()
        if not sku:
            QMessageBox.warning(self, 'Missing SKU', 'Please input SKU first.')
            return
        product = find_product_by_sku(sku)
        if not product:
            QMessageBox.warning(self, 'Not Found', f'No product found for SKU: {sku}')
            return
        self.fill_product_form(product)
        self.output.setPlainText(f'Loaded product from database:\n{sku}')

    def search_product_db(self):
        keyword = self.model.text().strip() or self.sku.text().strip() or self.brand.text().strip()
        products = search_products(keyword)
        if not products:
            self.output.setPlainText(f'No products found for keyword: {keyword}')
            return
        lines = [f"Found {len(products)} product(s) for keyword: {keyword}", '']
        for product in products[:50]:
            lines.append(f"SKU: {product.get('sku', '')} | {product.get('brand', '')} {product.get('model', '')} | {product.get('color', '')}")
        self.output.setPlainText('\n'.join(lines))

    def create_product_import_template_ui(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save Product Import Template',
            'Product_Import_Template.xlsx',
            'Excel Files (*.xlsx)'
        )
        if not path:
            return
        try:
            create_product_import_template(path)
            QMessageBox.information(self, 'Template Created', f'Product import template saved:\n{os.path.abspath(path)}')
        except Exception as error:
            QMessageBox.critical(self, 'Create Template Failed', str(error))

    def import_products_to_db_ui(self):
        input_file, _ = QFileDialog.getOpenFileName(
            self,
            'Select Product Import Excel',
            '',
            'Excel Files (*.xlsx *.xls)'
        )
        if not input_file:
            return
        try:
            imported = import_products_from_excel(input_file)
            QMessageBox.information(self, 'Import Complete', f'Imported / updated {len(imported)} product(s).')
            self.output.setPlainText('Imported products:\n\n' + '\n'.join(imported[:200]))
        except Exception as error:
            QMessageBox.critical(self, 'Import Failed', str(error))

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
            if not self.latest_markdown:
                self.generate()
            output_dir = export_material_package(product, root_dir)
            upsert_product(product)
            QMessageBox.information(self, 'Material Package Exported', f'Material package saved:\n{os.path.abspath(output_dir)}')
            self.output.setPlainText(
                f'Material package exported successfully.\n\nFolder:\n{output_dir}\n\nFiles:\n- listing.md\n- image_prompts.txt\n- assets.json\n\nProduct also saved to database.'
            )
        except Exception as error:
            QMessageBox.critical(self, 'Material Package Export Failed', str(error))

    def create_excel_template(self):
        default_name = 'AI_Ecommerce_Batch_Template.xlsx'
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save Listing Excel Template',
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
