from pathlib import Path


def export_psd_to_jpg(psd_path:str, output_jpg:str, text_layers:dict=None):
    try:
        import win32com.client
    except ImportError:
        raise RuntimeError('pywin32 is not installed. Run: pip install pywin32')

    text_layers = text_layers or {}

    app = win32com.client.Dispatch('Photoshop.Application')
    doc = app.Open(str(Path(psd_path).resolve()))

    for layer in doc.ArtLayers:
        try:
            if layer.Name in text_layers:
                layer.TextItem.Contents = str(text_layers[layer.Name])
        except Exception:
            pass

    jpg_options = win32com.client.Dispatch('Photoshop.JPEGSaveOptions')
    jpg_options.Quality = 12

    doc.SaveAs(str(Path(output_jpg).resolve()), jpg_options, True)
    doc.Close(2)

    return output_jpg


def render_amazon_main(product:dict, psd_template:str, output_jpg:str):
    title = f"{product.get('brand','')} {product.get('model','')}".strip()

    text_layers = {
        'TITLE': title,
        'SUBTITLE': product.get('switch',''),
        'SELLING_POINT_1': product.get('layout',''),
        'SELLING_POINT_2': product.get('connection','')
    }

    return export_psd_to_jpg(psd_template, output_jpg, text_layers)
