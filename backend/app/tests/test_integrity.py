from app.services.integrity import compute_content_hash, compute_chain_hash, verify_chain
from datetime import datetime

def test_chain_roundtrip():
    prev = "GENESIS"
    entries = []
    payloads = [
        ("Day 1", "Started experiment", ["lab","temp"], []),
        ("Day 2", "Added solvent", ["lab"], [{"sha256": "a"*64}]),
    ]
    for t,c,tags,atts in payloads:
        ch = compute_content_hash(t,c,tags,atts)
        cur = compute_chain_hash(prev, ch, datetime(2024,1,1,0,0,0))
        entries.append({
            "title": t, "content": c, "tags": tags, "attachments": atts,
            "timestamp": "2024-01-01T00:00:00", "content_hash": ch, "current_hash": cur
        })
        prev = cur
    assert verify_chain(entries) is True
