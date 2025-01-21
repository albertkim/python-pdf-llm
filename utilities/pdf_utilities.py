import aiohttp
import pymupdf
import base64
from io import BytesIO

async def _download_pdf_from_url(url: str) -> pymupdf.Document | None:
    try:
        async with aiohttp.ClientSession() as session:
            print(f"Downloading PDF from URL: {url}")
            async with session.get(url) as response:
                is_pdf = response.headers.get("content-type") == "application/pdf"
                if not is_pdf:
                    print(f"URL is not a valid PDF: {url}")
                    return None
                pdf_bytes = BytesIO(await response.content.read())
                pdf_document = pymupdf.open(stream=pdf_bytes, filetype="pdf")
                return pdf_document
    except aiohttp.ClientError as e:
        print(f"Error fetching URL: {e}")
        return None

async def _pdf_document_to_images(
    pdf_document: pymupdf.Document
) -> list[bytes]:
    page_images = [
        base64.b64encode(
            pdf_document.load_page(page_num)
            .get_pixmap()
            .tobytes("jpeg", jpg_quality=70)
        )
        for page_num in range(pdf_document.page_count)
    ]
    return page_images

async def pdf_url_to_images(url: str) -> list[bytes]:
    pdf_document = await _download_pdf_from_url(url)
    if not pdf_document:
        return []
    return await _pdf_document_to_images(pdf_document)
