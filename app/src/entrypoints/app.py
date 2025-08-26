import logging
from fastapi import FastAPI
from src.infra.controllers.states_controller import router as states_router
from src.infra.di.container import get_container

def app():
    """
    Cria e configura a aplicação FastAPI.
    
    Inicializa o container de dependências e configura
    todos os routers da aplicação.
    
    Returns:
        Instância configurada do FastAPI
    """
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Inicializa o container de dependências
    get_container()
                        
    app = FastAPI()        
    
    app.include_router(
        states_router,
        prefix="/api/v1",
        tags=["states"]
    )    
    
    return app
