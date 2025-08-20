import os, hashlib, pathlib
from fastapi import UploadFile
from typing import Tuple

DATA_DIR = pathlib.Path(os.environ.get("LL_DATA_DIR", __file__)).parent / "storage"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def sha256_stream(fileobj) -> str:
    h = hashlib.sha256()
    for chunk in iter(lambda: fileobj.read(8192), b""):
        h.update(chunk)
    fileobj.seek(0)
    return h.hexdigest()

def save_upload(file: UploadFile) -> Tuple[str, str]:
    # returns (sha256, path)
    sha = sha256_stream(file.file)
    sub = DATA_DIR / sha[:2]
    sub.mkdir(parents=True, exist_ok=True)
    dest = sub / f"{sha}_{file.filename}"
    with open(dest, "wb") as out:
        while True:
            chunk = file.file.read(8192)
            if not chunk: break
            out.write(chunk)
    return sha, str(dest)
