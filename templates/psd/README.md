# PSD Template System

This folder is used for PSD templates and PSD layer naming rules.

## Recommended PSD Layer Names

Use these layer names in Photoshop templates:

```text
PRODUCT_IMAGE
TITLE
SUBTITLE
SELLING_POINT_1
SELLING_POINT_2
SELLING_POINT_3
SELLING_POINT_4
SELLING_POINT_5
LOGO
BACKGROUND
BADGE
CTA
```

## Suggested Templates

```text
templates/psd/
├── amazon_main_1.psd
├── amazon_main_2.psd
├── amazon_aplus_1.psd
└── tiktok_showcase_1.psd
```

## Workflow

1. Prepare PSD template in Photoshop.
2. Name text/image layers according to the rules above.
3. Export product content from AI Ecommerce Center.
4. Use the PSD render engine to create JPG/PNG preview images.

## Current V9.1 Status

The project currently includes a PSD configuration layer and a Pillow-based placeholder renderer.
The next step is real PSD layer replacement through Photoshop automation or psd-tools integration.
