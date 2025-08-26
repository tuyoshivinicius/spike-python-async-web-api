"""
Módulo para integração do container DI com FastAPI.

Fornece dependências que podem ser usadas com o sistema de 
Dependency Injection do FastAPI através da função Depends().
"""

from fastapi import Depends
from typing import Any, Callable

from src.infra.di.container import resolve
from src.application.usecases.list_of_states_and_cities_usecase import ListOfStatesAndCities


def get_list_of_states_and_cities_usecase() -> ListOfStatesAndCities:
    """
    Dependency provider para o use case ListOfStatesAndCities.
    
    Esta função será usada com FastAPI Depends() para injetar
    automaticamente o use case nos endpoints.
    
    Returns:
        Instância configurada do use case
    """
    return resolve(ListOfStatesAndCities)


# Tipo para facilitar o uso nos controllers
ListOfStatesAndCitiesUseCase = Callable[[], ListOfStatesAndCities]
