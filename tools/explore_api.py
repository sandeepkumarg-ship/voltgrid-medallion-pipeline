"""Print one small page of an endpoint.
Run: PYTHONPATH=. python tools/explore_api.py /api/db/payments/
"""
import json
import sys

from config.settings import API_BASE_URL
from ingestion.http_client import login, make_session

path = sys.argv[1] if len(sys.argv) > 1 else "/api/auth/me/"
session = make_session(login())
resp = session.get(f"{API_BASE_URL}{path}", params={"page": 1, "page_size": 2}, timeout=30)
print("status:", resp.status_code)
print(json.dumps(resp.json(), indent=2)[:3000])
