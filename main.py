from typing import Annotated

from fastapi import FastAPI, Request, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

from core import upload_image, search_image
import os

app = FastAPI(
    title="Image Search",
    description="Multimodal Image Search powered by vector database",
    version="0.1.0"
)

# Set up templates directory
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "templates")
templates = Jinja2Templates(directory=templates_dir)

# Mount static files directory if it exists
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    """Serve the index.html page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload-images")
async def upload_images(file: Annotated[bytes, File()]):
    """Endpoint to handle image uploads"""
    # Here you would handle the uploaded files, e.g., save them or process them
    # For now, we just return a success message
    await upload_image(file)
    return {"message": "Images uploaded successfully", "file_count": len(file)}


@app.get("/search")
async def search_images(q: str):
    """Endpoint to search for images based on a query"""
    # Implement your search logic here
    # For now, we return a placeholder response
    results = await search_image(q)
    documents = []
    keys = set()
    for r in results:
        d, s = r
        if s < .51: continue
        if d.metadata.get("key") in keys: continue
        documents.append({
            "content": d.page_content,
            "metadata": d.metadata,
            "score": s
        })
        keys.add(d.metadata.get("key"))
        if len(keys) >= 10: break # Limit to 10 unique results
    return {"query": q, "results": documents}


@app.get("/uploads/{filename}")
async def get_image(filename: str):
    """Serve an image file from the static directory"""
    file_path = os.path.join("uploads", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
