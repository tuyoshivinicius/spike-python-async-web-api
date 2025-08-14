import asyncio
import aiohttp
from typing import List
import logging

from src.domain.dtos import DistrictDTO

logger = logging.getLogger("default")


class DistrictsGatewayError(Exception):
    """Exceção personalizada para erros do gateway de distritos"""
    pass


class DistrictsGateway:
    """Gateway para consumir dados de distritos do IBGE"""
    
    def __init__(self, base_url: str = "https://servicodados.ibge.gov.br/api/v1/localidades"):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=30)
    
    async def get_districts_by_city_id(self, city_id: int) -> List[DistrictDTO]:
        """
        Busca todos os distritos de uma cidade específica
        
        Args:
            city_id: ID da cidade
        
        Returns:
            Lista com DTOs de todos os distritos da cidade
            
        Raises:
            DistrictsGatewayError: Erro ao consumir a API
        """
        url = f"{self.base_url}/municipios/{city_id}/distritos"
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    if isinstance(data, list):
                        return [
                            DistrictDTO(
                                id=district.get('id', 0),
                                nome=district.get('nome', '')
                            ) for district in data
                        ]
                    return []
                    
        except aiohttp.ClientError as e:
            logger.error(f"Erro de conexão ao buscar distritos para cidade {city_id}: {e}")
            raise DistrictsGatewayError(f"Erro de conexão: {e}")
        except asyncio.TimeoutError:
            logger.error(f"Timeout ao buscar distritos para cidade {city_id}")
            raise DistrictsGatewayError("Timeout na requisição")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar distritos para cidade {city_id}: {e}")
            raise DistrictsGatewayError(f"Erro inesperado: {e}")
