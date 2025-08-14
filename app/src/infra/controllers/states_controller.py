from fastapi import APIRouter

from src.infra.gateways.states_gateway import StatesGateway
from src.infra.gateways.cities_gateway import CitiesGateway
from src.infra.gateways.districts_gateway import DistrictsGateway
from src.application.usecases.list_of_states_and_cities_usecase import ListOfStatesAndCities

router = APIRouter()

@router.get("/states")
async def get_states():
    states_gateway = StatesGateway()
    cities_gateway = CitiesGateway()
    districts_gateway = DistrictsGateway()

    # Configuração de concorrência: máximo 5 estados e 10 cidades simultaneamente
    usecase = ListOfStatesAndCities(
        states_gateway, 
        cities_gateway, 
        districts_gateway        
    )

    return await usecase.execute()