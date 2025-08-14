import logging
from fastapi import FastAPI
from src.infra.controllers.states_controller import router as states_router

def app():
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
                        
    app = FastAPI()        
    
    app.include_router(
        states_router,
        prefix="/api/v1",
        tags=["states"]
    )    
    
    return app
