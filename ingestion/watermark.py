"""Pure helpers for incremental loads (no Spark, no network, easy to test)."""
from datetime import datetime, timedelta, timezone


def parse_ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def since_param(watermark, lookback_min):
    """updated_after value = watermark minus lookback; None means full load."""
    if not watermark:
        return None
    since = parse_ts(watermark) - timedelta(minutes=lookback_min)
    return since.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def max_updated_at(records, current=None):
    stamps = [r["updated_at"] for r in records if r.get("updated_at")]
    if current:
        stamps.append(current)
    return max(stamps, key=parse_ts) if stamps else None