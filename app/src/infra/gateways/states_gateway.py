import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
import logging

from src.domain.dtos import StateDTO

logger = logging.getLogger("default")


class StatesGatewayError(Exception):
    """Exceção personalizada para erros do gateway de estados"""
    pass


class StatesGateway:
    """Gateway para consumir dados de estados do IBGE"""
    
    def __init__(self, base_url: str = "https://servicodados.ibge.gov.br/api/v1/localidades"):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=30)
    
    async def get_all_states(self) -> List[StateDTO]:
        """
        Busca todos os estados brasileiros
        
        Returns:
            Lista com DTOs de todos os estados
            
        Raises:
            StatesGatewayError: Erro ao consumir a API
        """
        url = f"{self.base_url}/estados"
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    if isinstance(data, list):
                        return [
                            StateDTO(
                                id=state.get('id', 0),
                                sigla=state.get('sigla', ''),
                                nome=state.get('nome', '')
                            ) for state in data
                        ]
                    return []
                    
        except aiohttp.ClientError as e:
            logger.error(f"Erro de conexão ao buscar estados: {e}")
            raise StatesGatewayError(f"Erro de conexão: {e}")
        except asyncio.TimeoutError:
            logger.error("Timeout ao buscar estados")
            raise StatesGatewayError("Timeout na requisição")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar estados: {e}")
            raise StatesGatewayError(f"Erro inesperado: {e}")    