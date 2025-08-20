from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import select
from typing import List
from datetime import datetime
from ..db import get_session
from ..models import JournalEntry, Attachment
from ..schemas import EntryCreate, EntryOut
from ..services.integrity import compute_content_hash, compute_chain_hash
from ..services.storage import save_upload

router = APIRouter(prefix="/entries", tags=["entries"])

@router.get("", response_model=List[EntryOut])
def list_entries(session=Depends(get_session)):
    rows = session.exec(select(JournalEntry).order_by(JournalEntry.id)).all()
    result = []
    for r in rows:
        atts = session.exec(select(Attachment).where(Attachment.entry_id==r.id)).all()
        result.append({
            "id": r.id, "title": r.title, "content": r.content,
            "tags": r.tags.split(",") if r.tags else [],
            "timestamp": r.timestamp.isoformat(),
            "prev_hash": r.prev_hash, "content_hash": r.content_hash,
            "current_hash": r.current_hash,
            "attachments": [ {"id": a.id, "filename": a.filename, "sha256": a.sha256, "path": a.path} for a in atts ]
        })
    return result

@router.post("", response_model=EntryOut)
def create_entry(payload: EntryCreate, session=Depends(get_session)):
    # get previous hash
    prev = "GENESIS"
    last = session.exec(select(JournalEntry).order_by(JournalEntry.id.desc())).first()
    if last:
        prev = last.current_hash
    timestamp = datetime.utcnow()
    content_hash = compute_content_hash(payload.title, payload.content, payload.tags, [])
    current_hash = compute_chain_hash(prev, content_hash, timestamp)

    entry = JournalEntry(
        title=payload.title,
        content=payload.content,
        tags=",".join(payload.tags),
        timestamp=timestamp,
        prev_hash=prev,
        content_hash=content_hash,
        current_hash=current_hash
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)

    return {
        "id": entry.id, "title": entry.title, "content": entry.content,
        "tags": payload.tags, "timestamp": timestamp.isoformat(),
        "prev_hash": prev, "content_hash": content_hash, "current_hash": current_hash,
        "attachments": []
    }

@router.post("/{entry_id}/attach", response_model=dict)
def attach_file(entry_id: int, file: UploadFile = File(...), session=Depends(get_session)):
    entry = session.get(JournalEntry, entry_id)
    if not entry:
        raise HTTPException(404, "Entry not found")
    sha, path = save_upload(file)
    att = Attachment(entry_id=entry_id, filename=file.filename, sha256=sha, path=path)
    session.add(att)
    session.commit()
    session.refresh(att)
    # update entry's hash by adding new attachment (append-only new hash)
    from ..services.integrity import compute_content_hash, compute_chain_hash
    from datetime import datetime
    atts = session.exec(select(Attachment).where(Attachment.entry_id==entry_id)).all()
    new_content = compute_content_hash(entry.title, entry.content, entry.tags.split(",") if entry.tags else [],
                                       [{"sha256": a.sha256} for a in atts])
    new_current = compute_chain_hash(entry.current_hash, new_content, datetime.utcnow())
    entry.prev_hash = entry.current_hash
    entry.content_hash = new_content
    entry.current_hash = new_current
    session.add(entry); session.commit(); session.refresh(entry)

    return {"attachment_id": att.id, "sha256": sha, "path": path}

@router.get("/verify", response_model=dict)
def verify_chain(session=Depends(get_session)):
    rows = session.exec(select(JournalEntry).order_by(JournalEntry.id)).all()
    prev = "GENESIS"
    for r in rows:
        from ..services.integrity import compute_chain_hash, compute_content_hash
        from datetime import datetime
        atts = session.exec(select(Attachment).where(Attachment.entry_id==r.id)).all()
        expected_content = compute_content_hash(r.title, r.content, r.tags.split(",") if r.tags else [],
                                                [{"sha256": a.sha256} for a in atts])
        if expected_content != r.content_hash:
            return {"ok": False, "at": r.id, "reason": "content_hash mismatch"}
        expected_current = compute_chain_hash(prev, r.content_hash, r.timestamp)
        if expected_current != r.current_hash:
            return {"ok": False, "at": r.id, "reason": "chain mismatch"}
        prev = r.current_hash
    return {"ok": True, "count": len(rows)}
