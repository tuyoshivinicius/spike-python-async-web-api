import asyncio
import logging
from typing import List, Any

logger = logging.getLogger('default')


class ListOfStatesAndCities:
    """Classe para buscar estados, cidades e distritos de forma assíncrona."""
    
    def __init__(self, states_gateway, cities_gateway, districts_gateway):
        self.states_gateway = states_gateway
        self.cities_gateway = cities_gateway
        self.districts_gateway = districts_gateway
        
        # Semáforos para controle de concorrência
        self.states_semaphore = asyncio.Semaphore(26)
        self.cities_semaphore = asyncio.Semaphore(500)

    async def execute(self) -> List[Any]:
        """Executa a busca completa de estados, cidades e distritos."""
        logger.info("Iniciando busca de estados, cidades e distritos")
        
        states = await self.states_gateway.get_all_states()
        logger.info(f"Encontrados {len(states)} estados")
        
        # Processa todos os estados em paralelo
        tasks = [self._process_state(state) for state in states]
        processed_states = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtra apenas os resultados válidos (não exceções)
        valid_states = [state for state in processed_states if not isinstance(state, Exception)]
        
        logger.info(f"Processamento concluído: {len(valid_states)} estados processados com sucesso")
        return valid_states

    async def _process_state(self, state) -> Any:
        """Processa um estado: busca suas cidades e distritos."""
        async with self.states_semaphore:
            try:
                logger.info(f"Processando estado: {state.nome}")
                
                # Busca cidades do estado
                cities = await self.cities_gateway.get_cities_by_uf(state.sigla)
                state.cidades = cities
                
                # Processa distritos de todas as cidades em paralelo
                if cities:
                    tasks = [self._process_city(city) for city in cities]
                    await asyncio.gather(*tasks, return_exceptions=True)
                
                logger.info(f"Estado {state.nome} processado: {len(cities)} cidades")
                return state
                
            except Exception as e:
                logger.error(f"Erro ao processar estado {state.nome}: {e}")
                raise

    async def _process_city(self, city) -> Any:
        """Processa uma cidade: busca seus distritos."""
        async with self.cities_semaphore:
            try:
                districts = await self.districts_gateway.get_districts_by_city_id(city.id)
                city.distritos = districts
                return city
                
            except Exception as e:
                logger.error(f"Erro ao processar cidade {city.nome}: {e}")
                raise

