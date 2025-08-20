import hashlib, json
from datetime import datetime

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def compute_content_hash(title: str, content: str, tags: list, attachments: list) -> str:
    canonical = json.dumps({
        "title": title,
        "content": content,
        "tags": sorted(tags),
        "attachments": sorted([a.get("sha256","") for a in attachments])
    }, separators=(",", ":"), ensure_ascii=False)
    return sha256_hex(canonical.encode("utf-8"))

def compute_chain_hash(prev_hash: str, content_hash: str, timestamp: datetime) -> str:
    payload = f"{prev_hash}|{content_hash}|{timestamp.isoformat()}".encode("utf-8")
    return sha256_hex(payload)

def verify_chain(entries: list) -> bool:
    prev = "GENESIS"
    for e in entries:
        expected_content = compute_content_hash(e["title"], e["content"], e.get("tags",[]), e.get("attachments",[]))
        if expected_content != e["content_hash"]:
            return False
        expected_current = compute_chain_hash(prev, e["content_hash"], datetime.fromisoformat(e["timestamp"]))
        if expected_current != e["current_hash"]:
            return False
        prev = e["current_hash"]
    return True
