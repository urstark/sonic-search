import os
import logging

import httpx
from py_yt.core.constants import userAgent

logger = logging.getLogger(__name__)

CLIENT_HEADERS = {
    "WEB": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-YouTube-Client-Name": "1",
        "X-YouTube-Client-Version": "2.20240726.00.00",
        "Origin": "https://www.youtube.com",
        "Referer": "https://www.youtube.com/",
        "Content-Type": "application/json",
    },
    "WEB_EMBEDDED": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-YouTube-Client-Name": "56",
        "X-YouTube-Client-Version": "2.20240726.01.00",
        "Origin": "https://www.youtube.com",
        "Referer": "https://www.youtube.com/",
        "Content-Type": "application/json",
    },
    "MWEB": {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "X-YouTube-Client-Name": "2",
        "X-YouTube-Client-Version": "2.20240726.01.00",
        "Origin": "https://www.youtube.com",
        "Content-Type": "application/json",
    },
    "TV_EMBED": {
        "User-Agent": "Mozilla/5.0 (SMART-TV; Linux; Tizen 5.0) AppleWebKit/538.1 (KHTML, like Gecko) Version/5.0 NativeTVs Safari/538.1",
        "X-YouTube-Client-Name": "85",
        "X-YouTube-Client-Version": "2.0",
        "Origin": "https://www.youtube.com",
        "Content-Type": "application/json",
    },
}

DEFAULT_HEADERS = {
    "User-Agent": userAgent,
    "X-YouTube-Client-Name": "1",
    "X-YouTube-Client-Version": "2.20240425.01.00",
    "Origin": "https://www.youtube.com",
}


class RequestCore:
    def __init__(self, timeout: float = 7.0, max_retries: int = 0):
        self.url: str | None = None
        self.data: dict | None = None
        self.timeout: float = timeout
        self.max_retries: int = max_retries
        self.proxy_url: str | None = os.environ.get("PROXY_URL")
        client_args = {"timeout": self.timeout, "proxy": self.proxy_url}

        self.async_client = httpx.AsyncClient(**client_args)

    async def asyncPostRequest(self, client_name: str = None) -> httpx.Response | None:
        """Sends an asynchronous POST request."""
        if not self.url:
            raise ValueError("URL must be set before making a request.")
        headers = CLIENT_HEADERS.get(client_name, DEFAULT_HEADERS) if client_name else DEFAULT_HEADERS
        for _ in range(self.max_retries + 1):
            try:
                response = await self.async_client.post(
                    self.url,
                    headers=headers,
                    json=self.data,
                )
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                logger.error(
                    "HTTP error during HTTP request",
                    extra={
                        "status_code": getattr(e.response, "status_code", None),
                        "response_text": getattr(e.response, "text", None),
                    },
                    exc_info=True,
                )
            except httpx.RequestError as e:
                logger.error(
                    "Request error during HTTP request",
                    extra={
                        "request_url": getattr(getattr(e, "request", None), "url", None),
                    },
                    exc_info=True,
                )
        return None

    async def asyncGetRequest(self) -> httpx.Response | None:
        """Sends an asynchronous GET request."""
        if not self.url:
            raise ValueError("URL must be set before making a request.")
        cookies = {"CONSENT": "YES+1"}
        for _ in range(self.max_retries + 1):
            try:
                response = await self.async_client.get(
                    self.url,
                    headers={"User-Agent": userAgent},
                    cookies=cookies,
                )
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                logger.error(
                    "HTTP error during HTTP request",
                    extra={
                        "status_code": getattr(e.response, "status_code", None),
                        "response_text": getattr(e.response, "text", None),
                    },
                    exc_info=True,
                )
            except httpx.RequestError as e:
                logger.error(
                    "Request error during HTTP request",
                    extra={
                        "request_url": getattr(getattr(e, "request", None), "url", None),
                    },
                    exc_info=True,
                )
        return None
