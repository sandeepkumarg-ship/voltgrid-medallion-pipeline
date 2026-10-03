import pytest

from ingestion import http_client


class FakeResp:
    def __init__(self, code):
        self.status_code, self.headers = code, {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(self.status_code)


class FakeSession:
    def __init__(self, codes):
        self.codes, self.calls = list(codes), 0

    def request(self, method, url, **kwargs):
        self.calls += 1
        return FakeResp(self.codes.pop(0))


def test_retries_then_succeeds(monkeypatch):
    monkeypatch.setattr(http_client.time, "sleep", lambda s: None)
    fake = FakeSession([429, 503, 200])
    resp = http_client.request_with_retry(fake, "GET", "http://x/api/db/payments/")
    assert resp.status_code == 200 and fake.calls == 3


def test_fails_fast_on_404(monkeypatch):
    monkeypatch.setattr(http_client.time, "sleep", lambda s: None)
    fake = FakeSession([404])
    with pytest.raises(RuntimeError):
        http_client.request_with_retry(fake, "GET", "http://x/")
    assert fake.calls == 1
