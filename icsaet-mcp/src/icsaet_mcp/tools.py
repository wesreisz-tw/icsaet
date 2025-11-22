"""MCP tools for ICAET query operations."""

import httpx
import logging

from .server import ICAET_API_KEY, USER_EMAIL, mcp
from .utils import sanitize_question

logger = logging.getLogger(__name__)


async def _query_impl(question: str, api_key: str, user_email: str) -> dict:
    """Implementation of query logic for testability.
    
    Args:
        question: The question to ask the ICAET knowledge base
        api_key: API key for authentication
        user_email: User email for the request
        
    Returns:
        API response as a dictionary, or error dict if request fails
    """
    logger.info(f"Query received [question_length={len(question)}]")
    logger.debug(f"Query question [question={sanitize_question(question, max_len=100)}]")
    
    url = "https://icaet-dev.wesleyreisz.com/query"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    body = {
        "email": user_email,
        "question": question
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=body, headers=headers)
            response.raise_for_status()
            logger.info(f"API request successful [status_code={response.status_code}]")
            logger.debug(f"API response [response_size={len(response.text)} bytes]")
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"API request failed [status_code={e.response.status_code}, error=HTTPStatusError]")
        return {"error": f"API error {e.response.status_code}: {e.response.text}"}
    except httpx.RequestError as e:
        logger.error(f"API request failed [error=RequestError, message={str(e)}]")
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        logger.error(f"API request failed [error=UnexpectedException, message={str(e)}]")
        return {"error": f"Unexpected error: {str(e)}"}


@mcp.tool()
async def query(question: str) -> dict:
    """Query the ICAET knowledge base with a question.
    
    Args:
        question: The question to ask the ICAET knowledge base
        
    Returns:
        API response as a dictionary, or error dict if request fails
    """
    return await _query_impl(question, ICAET_API_KEY, USER_EMAIL)

