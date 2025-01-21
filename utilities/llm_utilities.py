import os
import asyncio
from openai import AsyncOpenAI
from typing import Literal
from dotenv import load_dotenv
from pdf_utilities import pdf_url_to_images

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

OPENAI_API_URL = "https://api.openai.com/v1"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"
XAI_API_URL = "https://api.xai.com/v1"

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_URL) if OPENAI_API_KEY else None
anthropic_client = AsyncOpenAI(api_key=ANTHROPIC_API_KEY, base_url=ANTHROPIC_API_URL) if ANTHROPIC_API_KEY else None
deepseek_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL) if DEEPSEEK_API_KEY else None
xai_client = AsyncOpenAI(api_key=XAI_API_KEY, base_url=XAI_API_URL) if XAI_API_KEY else None

def _get_client(llm_provider: Literal["openai", "anthropic", "deepseek", "xai"]) -> AsyncOpenAI:
    if llm_provider == "openai":
        return openai_client
    elif llm_provider == "anthropic":
        return anthropic_client
    elif llm_provider == "deepseek":
        return deepseek_client
    elif llm_provider == "xai":
        return xai_client
    else:
        raise ValueError(f"Invalid LLM provider: {llm_provider}")

async def get_llm_text_response(llm_provider: Literal["openai", "anthropic", "deepseek", "xai"], model: str, prompt: str, image: str | bytes | None = None) -> str:
    client = _get_client(llm_provider)
    
    messages = [{"role": "user", "content": prompt}]
    if image:
        # Add image content to message if provided
        messages[0]["content"] = [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": image if isinstance(image, str) else f"data:image/jpeg;base64,{image}"
                }
            }
        ]
    
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content

async def get_llm_text_response_from_pdf(llm_provider: Literal["openai", "anthropic", "deepseek", "xai"], model: str, prompt: str, pdf_url: str, concurrent_requests: int = 5) -> list[str]:
    pdf_images = await pdf_url_to_images(pdf_url)
    if not pdf_images:
        return []
        
    async def process_page(image: bytes) -> str:
        return await get_llm_text_response(
            llm_provider=llm_provider,
            model=model, 
            prompt=prompt,
            image=image
        )
    
    sem = asyncio.Semaphore(concurrent_requests)
    
    async def process_with_semaphore(image: bytes) -> str:
        async with sem:
            return await process_page(image)
    
    # Process all pages concurrently with semaphore
    responses = await asyncio.gather(
        *[process_with_semaphore(image) for image in pdf_images]
    )
    
    return responses
