from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL


def generate_ai_markdown(product: dict) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY is missing. Please create a .env file first.')

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
You are an expert cross-border ecommerce listing copywriter.
Create high-quality ecommerce material for this product.

Product information:
{product}

Requirements:
1. Output in Markdown.
2. Include Amazon title, 5 bullet points, product description, A+ modules, TEMU selling points, TikTok Shop selling points, main image copy, A+ image copy, and image generation prompts.
3. Use natural English suitable for Amazon / TEMU / TikTok Shop.
4. Do not make unsupported certifications or impossible claims.
5. Keep the content practical for keyboard / mouse / gaming peripheral ecommerce operations.
"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {'role': 'system', 'content': 'You are a senior ecommerce content strategist for gaming peripherals.'},
            {'role': 'user', 'content': prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content
