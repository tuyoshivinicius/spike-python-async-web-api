from abc import ABC, abstractmethod
from typing import List

from src.domain.dtos import StateDTO, CityDTO, DistrictDTO


class StatesGatewayPortInterface(ABC):
    """Interface para o gateway de estados"""
    
    @abstractmethod
    async def get_all_states(self) -> List[StateDTO]:
        """
        Busca todos os estados brasileiros
        
        Returns:
            Lista com DTOs de todos os estados
        """
        pass


class CitiesGatewayPortInterface(ABC):
    """Interface para o gateway de cidades"""
    
    @abstractmethod
    async def get_cities_by_uf(self, uf: str) -> List[CityDTO]:
        """
        Busca todas as cidades de um estado específico
        
        Args:
            uf: Sigla do estado (ex: 'SP', 'RJ')
        
        Returns:
            Lista com DTOs de todas as cidades do estado
        """
        pass


class DistrictsGatewayPortInterface(ABC):
    """Interface para o gateway de distritos"""
    
    @abstractmethod
    async def get_districts_by_city_id(self, city_id: int) -> List[DistrictDTO]:
        """
        Busca todos os distritos de uma cidade específica
        
        Args:
            city_id: ID da cidade
        
        Returns:
            Lista com DTOs de todos os distritos da cidade
        """
        pass