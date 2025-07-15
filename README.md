# Multimodal Image Search

## Overview
This project implements a multimodal image search system powered by vector databases. Users can upload an image or enter a text prompt to find visually or semantically similar images using embeddings and similarity search techniques.

## Features
- **Image Search Interface**: Clean, responsive UI for searching images
- **Text-based Search**: Find images using natural language queries
- **FastAPI Backend**: Modern, high-performance Python web framework
- **Vector Database Integration**: Efficient similarity search using vector embeddings

## Getting Started

### Prerequisites
- Python 3.11 or higher
- pip or another package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/7xAI-challenge-day2-image-search.git
cd 7xAI-challenge-day2-image-search
```

2. Install dependencies:
```bash
pip install -e .
```

### Running the Application

Start the FastAPI server:
```bash
python main.py
```

The application will be available at http://localhost:8000

You can also run it using uvicorn directly:
```bash
uvicorn main:app --reload
```

### API Documentation

Once the server is running, you can access the automatic API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure
```
7xAI-challenge-day2-image-search/
├── main.py                # FastAPI application entry point
├── public/                # Public assets
│   └── templates/         # HTML templates
│       └── index.html     # Main search interface
├── pyproject.toml         # Project dependencies and metadata
└── README.md              # This file
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is open source and available under the [CC0 1.0 Universal License](LICENSE).
