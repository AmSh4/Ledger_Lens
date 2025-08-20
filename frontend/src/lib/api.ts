const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function listEntries() {
  const r = await fetch(`${API}/entries`)
  return r.json()
}

export async function createEntry(payload: {title: string, content: string, tags: string[]}) {
  const r = await fetch(`${API}/entries`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  })
  return r.json()
}

export async function verifyChain() {
  const r = await fetch(`${API}/entries/verify`)
  return r.json()
}

export async function attachFile(entryId: number, file: File) {
  const fd = new FormData()
  fd.append('file', file)
  const r = await fetch(`${API}/entries/${entryId}/attach`, { method: 'POST', body: fd })
  return r.json()
}
