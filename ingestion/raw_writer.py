"""Land API pages as JSONL files, never leaving half a file behind."""
import json
import shutil
from pathlib import Path


def write_jsonl(folder, name, records):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    tmp = folder / f".{name}.tmp"  # hidden: Spark skips '.' and '_' files
    with tmp.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, default=str) + "\n")
    dest = folder / name
    shutil.move(str(tmp), str(dest), copy_function=shutil.copyfile)  # rename, or copy and delete
    return dest


def raw_page_path(root, source, entity, ingest_date):
    return Path(root) / source / entity / f"ingest_date={ingest_date}"