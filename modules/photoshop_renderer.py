from pathlib import Path


PHOTOSHOP_DONOTSAVECHANGES = 2


def _get_photoshop_app():
    try:
        import win32com.client
    except ImportError:
        raise RuntimeError('pywin32 is not installed. Run: pip install pywin32')

    return win32com.client.Dispatch('Photoshop.Application'), win32com.client


def _iter_art_layers(container):
    for layer in container.ArtLayers:
        yield layer

    for group in container.LayerSets:
        yield from _iter_art_layers(group)


def _replace_text_layers(doc, text_layers: dict):
    for layer in _iter_art_layers(doc):
        try:
            if layer.Name in text_layers:
                layer.TextItem.Contents = str(text_layers[layer.Name])
        except Exception:
            pass


def _place_product_image(app, image_path: str):
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f'Product image not found: {image_path}')

    # Photoshop JavaScript: place image as smart object into active document.
    jsx = f"""
var fileRef = new File('{str(image_path.resolve()).replace('\\', '/')}');
var desc = new ActionDescriptor();
desc.putPath(charIDToTypeID('null'), fileRef);
desc.putEnumerated(charIDToTypeID('FTcs'), charIDToTypeID('QCSt'), charIDToTypeID('Qcsa'));
executeAction(charIDToTypeID('Plc '), desc, DialogModes.NO);
app.activeDocument.activeLayer.name = 'PRODUCT_IMAGE_PLACED';
"""
    app.DoJavaScript(jsx)


def export_psd_to_jpg(psd_path: str, output_jpg: str, text_layers: dict = None, product_image: str = None):
    app, win32com = _get_photoshop_app()
    text_layers = text_layers or {}

    psd_path = Path(psd_path).resolve()
    output_jpg = Path(output_jpg).resolve()
    output_jpg.parent.mkdir(parents=True, exist_ok=True)

    doc = app.Open(str(psd_path))

    try:
        _replace_text_layers(doc, text_layers)

        if product_image:
            _place_product_image(app, product_image)

        jpg_options = win32com.client.Dispatch('Photoshop.JPEGSaveOptions')
        jpg_options.Quality = 12
        doc.SaveAs(str(output_jpg), jpg_options, True)
    finally:
        doc.Close(PHOTOSHOP_DONOTSAVECHANGES)

    return str(output_jpg)


def build_main_text_layers(product: dict):
    title = f"{product.get('brand', '')} {product.get('model', '')}".strip()
    return {
        'TITLE': title,
        'SUBTITLE': product.get('switch', ''),
        'SELLING_POINT_1': product.get('layout', ''),
        'SELLING_POINT_2': product.get('connection', ''),
        'SELLING_POINT_3': product.get('rgb', ''),
    }


def render_amazon_main(product: dict, psd_template: str, output_jpg: str, product_image: str = None):
    text_layers = build_main_text_layers(product)
    return export_psd_to_jpg(psd_template, output_jpg, text_layers, product_image)


def batch_render_psd(products: list, psd_template: str, output_dir: str, image_dir: str = None):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    image_dir_path = Path(image_dir) if image_dir else None

    rendered_files = []

    for product in products:
        model = product.get('model', 'product').replace(' ', '_')
        output_jpg = output_dir / f'{model}_Main_1.jpg'

        product_image = None
        if image_dir_path:
            for ext in ['.png', '.jpg', '.jpeg', '.webp']:
                candidate = image_dir_path / f'{model}{ext}'
                if candidate.exists():
                    product_image = str(candidate)
                    break

        rendered_files.append(
            render_amazon_main(product, psd_template, str(output_jpg), product_image)
        )

    return rendered_files
