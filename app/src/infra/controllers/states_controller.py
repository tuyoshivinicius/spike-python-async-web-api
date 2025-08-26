from fastapi import APIRouter, Depends

from src.application.usecases.list_of_states_and_cities_usecase import ListOfStatesAndCities
from src.infra.di.dependencies import get_list_of_states_and_cities_usecase

router = APIRouter()

@router.get("/states")
async def get_states(
    usecase: ListOfStatesAndCities = Depends(get_list_of_states_and_cities_usecase)
):
    """
    Endpoint para buscar todos os estados com suas respectivas cidades e distritos.
    
    As dependências são injetadas automaticamente pelo container DI.
    
    Returns:
        Lista com todos os estados, cidades e distritos
    """
    return await usecase.execute()