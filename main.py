from fastapi import FastAPI
from supabase import create_client
import os

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def home():
    return {"memory_engine": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/search_memory")
def search_memory(query: str):

    result = supabase.rpc(
        "search_memory",
        {"query_text": query}
    ).execute()

    return result.data


@app.post("/write_memory")
def write_memory(content: str, area: str, importance: float):

    data = {
        "content": content,
        "area": area,
        "importance": importance
    }

    result = supabase.table("memories").insert(data).execute()

    return result.data
