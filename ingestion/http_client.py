import random
import time

import requests

from config.logger import get_logger
from config.settings import API_BASE_URL, API_PASSWORD, API_USERNAME, MAX_RETRIES

logger = get_logger("http")

RETRYABLE = {429, 500, 502, 503, 504}


def request_with_retry(session, method, url, max_retries=MAX_RETRIES, base_delay=1.0, **kw):
    for attempt in range(1, max_retries + 1):
        try:
            resp = session.request(method, url, timeout=30, **kw)
        except (requests.ConnectionError, requests.Timeout) as exc:
            resp, error = None, repr(exc)
        else:
            if resp.status_code not in RETRYABLE:
                resp.raise_for_status()  # other 4xx = our bug, stop now
                return resp
            error = f"HTTP {resp.status_code}"
        wait = resp.headers.get("Retry-After") if resp is not None else None
        if wait and wait.isdigit():
            delay = float(wait)
        else:
            delay = base_delay * 2 ** (attempt - 1) + random.uniform(0, 0.5)
        logger.warning(f"{error} {url} attempt {attempt}/{max_retries}, sleep {delay:.1f}s")
        time.sleep(delay)
    raise RuntimeError(f"Gave up after {max_retries} attempts: {url}")


def login():
    with requests.Session() as s:
        r = request_with_retry(
            s, "POST", f"{API_BASE_URL}/api/auth/login/",
            json={"username": API_USERNAME, "password": API_PASSWORD},
        )
    return r.json()["token"]


def make_session(token):
    s = requests.Session()
    s.headers.update({"Authorization": f"Token {token}"})
    return s
