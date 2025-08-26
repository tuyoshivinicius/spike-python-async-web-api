import asyncio
import aiohttp
from typing import List
import logging

from src.domain.dtos import CityDTO
from src.application.ports import CitiesGatewayPortInterface

logger = logging.getLogger("default")


class CitiesGatewayError(Exception):
    """Exceção personalizada para erros do gateway de cidades"""
    pass


class CitiesGateway(CitiesGatewayPortInterface):
    """Gateway para consumir dados de cidades do IBGE"""
    
    def __init__(self, base_url: str = "https://servicodados.ibge.gov.br/api/v1/localidades"):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=30)
    
    async def get_cities_by_uf(self, uf: str) -> List[CityDTO]:
        """
        Busca todas as cidades de um estado específico
        
        Args:
            uf: Sigla do estado (ex: 'SP', 'RJ')
        
        Returns:
            Lista com DTOs de todas as cidades do estado
            
        Raises:
            CitiesGatewayError: Erro ao consumir a API
        """
        url = f"{self.base_url}/estados/{uf.upper()}/municipios"
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    if isinstance(data, list):
                        return [
                            CityDTO(
                                id=city.get('id', 0),
                                nome=city.get('nome', '')
                            ) for city in data
                        ]
                    return []
                    
        except aiohttp.ClientError as e:
            logger.error(f"Erro de conexão ao buscar cidades para UF {uf}: {e}")
            raise CitiesGatewayError(f"Erro de conexão: {e}")
        except asyncio.TimeoutError:
            logger.error(f"Timeout ao buscar cidades para UF {uf}")
            raise CitiesGatewayError("Timeout na requisição")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar cidades para UF {uf}: {e}")
            raise CitiesGatewayError(f"Erro inesperado: {e}")