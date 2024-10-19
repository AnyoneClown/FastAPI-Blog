import logging

from backend.app.api.deps import model

logger = logging.getLogger(__name__)


async def moderate_content(content: str) -> bool:
    prompt = f"Is the following content appropriate and free from profanity or offensive language? Content: '{content}' Please, answer in format: 'offensive' or 'Normal'"
    response = await model.generate_content_async(prompt)
    response_text = response.text.lower()
    if "offensive" in response_text:
        return False
    return True
