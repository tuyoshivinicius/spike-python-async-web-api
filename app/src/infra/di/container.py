"""
Módulo de configuração do container de Dependency Injection usando punq.

Este módulo é responsável por configurar e fornecer o container DI
que será usado em toda a aplicação para resolução de dependências.
"""

import punq
from typing import Any

from src.application.ports import (
    StatesGatewayPortInterface,
    CitiesGatewayPortInterface, 
    DistrictsGatewayPortInterface
)
from src.application.usecases.list_of_states_and_cities_usecase import ListOfStatesAndCities
from src.infra.gateways.states_gateway import StatesGateway
from src.infra.gateways.cities_gateway import CitiesGateway
from src.infra.gateways.districts_gateway import DistrictsGateway


def create_container() -> punq.Container:
    """
    Cria e configura o container de Dependency Injection.
    
    Registra todas as dependências necessárias para a aplicação,
    incluindo gateways e use cases.
    
    Returns:
        Container configurado com todas as dependências
    """
    container = punq.Container()
    
    # Registra os gateways como implementações das interfaces
    container.register(StatesGatewayPortInterface, StatesGateway, scope=punq.Scope.singleton)
    container.register(CitiesGatewayPortInterface, CitiesGateway, scope=punq.Scope.singleton)
    container.register(DistrictsGatewayPortInterface, DistrictsGateway, scope=punq.Scope.singleton)
    
    # Registra o use case
    container.register(ListOfStatesAndCities, scope=punq.Scope.transient)
    
    return container


# Container global da aplicação
_container: punq.Container = None


def get_container() -> punq.Container:
    """
    Obtém a instância global do container DI.
    
    Returns:
        Container de dependências configurado
    """
    global _container
    if _container is None:
        _container = create_container()
    return _container


def resolve(service_type: type) -> Any:
    """
    Resolve uma dependência do container.
    
    Args:
        service_type: Tipo da dependência a ser resolvida
        
    Returns:
        Instância da dependência resolvida
    """
    container = get_container()
    return container.resolve(service_type)
