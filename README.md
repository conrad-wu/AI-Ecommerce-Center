# AI Ecommerce Center

AI Ecommerce Center 是一个面向跨境电商运营的素材生成工具，用于快速生成 Amazon、TEMU、TikTok Shop、AliExpress 等平台的商品标题、五点描述、A+ 页面文案、主图卖点文案和图片提示词。

## 第一版功能

- Amazon 标题生成
- Amazon 五点描述生成
- 产品描述生成
- A+ 页面模块文案生成
- TEMU 卖点生成
- TikTok Shop 卖点生成
- 主图 / A+ 图片提示词生成
- 输出结果保存为 Markdown 文件

## 适用场景

- AJAZZ / NACODEX 键盘、鼠标、键帽、掌托等产品上架
- Amazon Listing 文案优化
- TEMU / TikTok Shop 商品卖点整理
- A+ 页面设计前的文案规划
- 主图和场景图生成提示词整理

## 快速开始

```bash
pip install -r requirements.txt
python app.py
```

## 环境变量

请在本地创建 `.env` 文件：

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

## 当前项目结构

```text
AI-Ecommerce-Center/
├── app.py
├── config.py
├── requirements.txt
├── modules/
│   ├── __init__.py
│   └── content_generator.py
├── templates/
│   └── sample_product.json
└── output/
```
