from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(
    title="Image Search App",
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
