from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    """
    Adds CORS middleware to the FastAPI app to allow frontend communication.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Allow frontend origin
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
        allow_headers=["*"],  # Allow all headers
    )
