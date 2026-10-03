"""Read every page of an API endpoint, one page at a time."""
import time

from ingestion.http_client import logger, request_with_retry

ENDPOINTS = {
    "payments": "/api/db/payments/",
    "fleet": "/api/db/fleet/",
    "weather": "/api/db/weather/",
}


def fetch_pages(session, base_url, path, page_size=1000, params=None, delay=0.3, max_pages=None):
    """Generator: yields (page_no, records) one page at a time."""
    page = 1
    while True:
        query = {"page": page, "page_size": page_size, **(params or {})}
        body = request_with_retry(session, "GET", f"{base_url}{path}", params=query).json()
        total_pages = body["pagination"]["total_pages"]
        records = body["data"]
        logger.info(f"{path} page {page}/{total_pages} - {len(records)} rows")
        yield page, records
        if page >= total_pages or (max_pages and page >= max_pages):
            break
        page += 1
        time.sleep(delay)  # be polite: rate limiting on our side