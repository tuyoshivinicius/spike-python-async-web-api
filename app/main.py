import uvicorn
from src.entrypoints.app import app

def create_app():
    return app()

if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        host="0.0.0.0",
        port=8001,
        reload=True        
    )