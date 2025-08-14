# Spike Python Async Web API

## Introdução

Este repositório é um **spike educacional** que demonstra como construir e executar **aplicações Web API assíncronas** seguindo o padrão **ASGI** (Asynchronous Server Gateway Interface) utilizando Python e bibliotecas modernas.

O projeto serve como um exemplo prático de como implementar APIs performáticas e escaláveis usando programação assíncrona, sendo especialmente útil para cenários que envolvem múltiplas chamadas a APIs externas ou operações I/O intensivas.

### Contexto

No desenvolvimento de APIs modernas, especialmente aquelas que precisam integrar com múltiplos serviços externos, a programação assíncrona se torna essencial para:

- **Melhorar a performance**: Evitando bloqueios desnecessários durante operações I/O
- **Aumentar a escalabilidade**: Permitindo que uma única thread processe múltiplas requisições
- **Otimizar recursos**: Reduzindo o uso de memória e CPU em operações de espera

### Potencial como Boilerplate

Este spike pode ser utilizado como base para projetos que necessitem:

- Integração assíncrona com APIs REST externas
- Processamento paralelo de grandes volumes de dados
- Arquitetura limpa e bem estruturada para APIs Python
- Controle de concorrência e rate limiting
- Tratamento robusto de erros em operações assíncronas

## Arquitetura e Stack Técnica

### Stack Principal

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno e rápido para construção de APIs, com suporte nativo a async/await e documentação automática via OpenAPI
- **[uvicorn](https://www.uvicorn.org/)**: Servidor ASGI de alta performance para executar aplicações FastAPI em produção
- **[aiohttp](https://docs.aiohttp.org/)**: Cliente HTTP assíncrono para realizar requisições a APIs externas de forma não-bloqueante

### Arquitetura em Camadas

O projeto segue os princípios da **Clean Architecture**, organizando o código em camadas bem definidas:

```
app/src/
├── entrypoints/          # Camada de Entrada
├── application/          # Camada de Aplicação  
├── domain/              # Camada de Domínio
└── infra/               # Camada de Infraestrutura
```

#### Entrypoints (`entrypoints/`)
Responsável pela configuração da aplicação FastAPI e definição das rotas principais.

```python
# src/entrypoints/app.py
def app():
    app = FastAPI()        
    app.include_router(
        states_router,
        prefix="/api/v1",
        tags=["states"]
    )    
    return app
```

#### Application (`application/`)
Contém a lógica de negócio e orquestração de operações assíncronas. Implementa os casos de uso da aplicação.

```python
# Exemplo de controle de concorrência
self.states_semaphore = asyncio.Semaphore(26)
self.cities_semaphore = asyncio.Semaphore(500)
```

#### Domain (`domain/`)
Define as estruturas de dados utilizadas pela aplicação através de DTOs (Data Transfer Objects) tipados.

```python
@dataclass
class StateDTO:
    id: int
    sigla: str
    nome: str
    cidades: Optional[List[CityDTO]] = None
```

#### Infra (`infra/`)
Implementa a integração com sistemas externos, dividida em:

- **Controllers**: Definem os endpoints REST e fazem a ponte com os casos de uso
- **Gateways**: Realizam a comunicação assíncrona com APIs externas (IBGE)

## Conceitos Aplicados

### Padrão ASGI (Asynchronous Server Gateway Interface)

O projeto utiliza o padrão ASGI, que é a evolução assíncrona do WSGI, permitindo:

- Suporte nativo a WebSockets e HTTP/2
- Processamento assíncrono de requisições
- Melhor utilização de recursos do servidor

```python
# main.py - Configuração do servidor ASGI
uvicorn.run(
    "main:create_app",
    host="0.0.0.0",
    port=8001,
    reload=True        
)
```

### async/await e Concorrência com asyncio

Toda a aplicação é construída sobre programação assíncrona, utilizando as palavras-chave `async` e `await`:

```python
@router.get("/states")
async def get_states():
    # Endpoint assíncrono
    return await usecase.execute()

async def get_all_states(self) -> List[StateDTO]:
    # Gateway assíncrono
    async with aiohttp.ClientSession(timeout=self.timeout) as session:
        async with session.get(url) as response:
            return await response.json()
```

### Controle de Acesso com Semaphores

Para evitar sobrecarga das APIs externas, o projeto implementa controle de concorrência usando semáforos:

```python
class ListOfStatesAndCities:
    def __init__(self, states_gateway, cities_gateway, districts_gateway):
        # Limita o processamento simultâneo de estados
        self.states_semaphore = asyncio.Semaphore(26)
        # Limita o processamento simultâneo de cidades  
        self.cities_semaphore = asyncio.Semaphore(500)

    async def _process_state(self, state):
        async with self.states_semaphore:
            # Processa estado de forma controlada
            cities = await self.cities_gateway.get_cities_by_uf(state.sigla)
```

### Processamento Paralelo com asyncio.gather()

O projeto demonstra como executar múltiplas operações assíncronas em paralelo:

```python
async def execute(self) -> List[Any]:
    states = await self.states_gateway.get_all_states()
    
    # Processa todos os estados em paralelo
    tasks = [self._process_state(state) for state in states]
    processed_states = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filtra apenas os resultados válidos
    valid_states = [state for state in processed_states 
                   if not isinstance(state, Exception)]
```

### Integração com APIs Externas via Clientes HTTP Assíncronos

Utiliza `aiohttp` para realizar requisições HTTP de forma não-bloqueante:

```python
async with aiohttp.ClientSession(timeout=self.timeout) as session:
    async with session.get(url) as response:
        response.raise_for_status()
        data = await response.json()
```

### Tratamento Robusto de Exceções

Implementa tratamento específico para diferentes tipos de erros:

```python
try:
    # Operação assíncrona
    async with session.get(url) as response:
        return await response.json()
except aiohttp.ClientError as e:
    logger.error(f"Erro de conexão: {e}")
    raise StatesGatewayError(f"Erro de conexão: {e}")
except asyncio.TimeoutError:
    logger.error("Timeout ao buscar estados")
    raise StatesGatewayError("Timeout na requisição")
```

## Como Executar

### Pré-requisitos

- Python 3.11+ instalado
- pip (gerenciador de pacotes Python)

### Passo a Passo

#### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd spike-python-async-web-api
```

#### 2. Criar e Ativar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Linux/Mac
source venv/bin/activate

# Ativar no Windows
venv\Scripts\activate
```

#### 3. Instalar Dependências

```bash
cd app
pip install -r requirements.txt
```

#### 4. Executar a Aplicação

##### Opção 1: Execução Padrão (Linux/Mac/Windows)

```bash
python main.py
```

##### Opção 2: Usando uvicorn diretamente

```bash
uvicorn main:create_app --host 0.0.0.0 --port 8001 --reload
```

##### Opção 3: Windows com múltiplos workers

```bash
# Executar o arquivo start.bat
start.bat

# Ou diretamente:
uvicorn main:create_app --workers=4
```

### Acessando a API

Após a execução, a API estará disponível em:

- **URL Base**: http://localhost:8001
- **Documentação Interativa (Swagger)**: http://localhost:8001/docs
- **Documentação Alternativa (ReDoc)**: http://localhost:8001/redoc

### Endpoint Disponível

```
GET /api/v1/states
```

Este endpoint retorna todos os estados brasileiros com suas respectivas cidades e distritos, processados de forma assíncrona e paralela.

## Fluxo de Execução

### Inicialização da Aplicação

1. **Carregamento do Módulo**: O `main.py` importa e configura a aplicação FastAPI
2. **Configuração do Servidor**: uvicorn inicia o servidor ASGI na porta 8001
3. **Registro de Rotas**: A aplicação registra as rotas do controller de estados
4. **Configuração de Logging**: Sistema de logs é configurado para monitoramento

### Processamento de Requisições

Quando uma requisição é feita para `/api/v1/states`, o seguinte fluxo ocorre:

```
1. Requisição HTTP → FastAPI Router
2. Controller → Instancia Gateways e UseCase  
3. UseCase → Orquestra operações assíncronas
4. Processamento Paralelo:
   ├── Busca todos os estados (API IBGE)
   ├── Para cada estado: busca cidades (paralelo)
   └── Para cada cidade: busca distritos (paralelo)
5. Agregação → Monta estrutura hierárquica
6. Resposta JSON → Cliente
```

### Detalhamento do Processamento Assíncrono

#### Fase 1: Busca de Estados
```python
# Requisição única para obter todos os estados
states = await self.states_gateway.get_all_states()
```

#### Fase 2: Processamento Paralelo de Estados
```python
# Cria uma task para cada estado
tasks = [self._process_state(state) for state in states]
# Executa todas as tasks em paralelo
processed_states = await asyncio.gather(*tasks, return_exceptions=True)
```

#### Fase 3: Processamento Paralelo de Cidades (por estado)
```python
# Para cada estado, processa suas cidades em paralelo
if cities:
    tasks = [self._process_city(city) for city in cities]
    await asyncio.gather(*tasks, return_exceptions=True)
```

### Controle de Concorrência

O sistema implementa dois níveis de controle:

- **Semáforo de Estados** (26): Limita o processamento simultâneo de estados
- **Semáforo de Cidades** (500): Controla as requisições para buscar distritos

Isso evita sobrecarregar a API do IBGE e garante estabilidade do sistema.

### Tratamento de Erros

- **Exceções de Rede**: Capturadas e logadas, não interrompem o processamento de outros itens
- **Timeouts**: Configurados para 30 segundos por requisição
- **Filtragem de Resultados**: Apenas dados válidos são retornados ao cliente

## Referências

### Documentação Oficial

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno para Python
- **[uvicorn](https://www.uvicorn.org/)** - Servidor ASGI de alta performance
- **[aiohttp](https://docs.aiohttp.org/)** - Cliente HTTP assíncrono
- **[asyncio](https://docs.python.org/3/library/asyncio.html)** - Programação assíncrona em Python

### Conceitos e Padrões

- **[ASGI Specification](https://asgi.readthedocs.io/)** - Especificação do padrão ASGI
- **[Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)** - Princípios de arquitetura limpa
- **[Python Async/Await](https://docs.python.org/3/library/asyncio-task.html)** - Guia oficial de async/await

### APIs Utilizadas

- **[API IBGE Localidades](https://servicodados.ibge.gov.br/api/docs/localidades)** - Dados geográficos do Brasil

### Tutoriais e Artigos Relevantes

- **[FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)** - Tutorial oficial do FastAPI
- **[Real Python - Async IO](https://realpython.com/async-io-python/)** - Guia completo de programação assíncrona
- **[Concurrency in Python](https://realpython.com/python-concurrency/)** - Conceitos de concorrência em Python
