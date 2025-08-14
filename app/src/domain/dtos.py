from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DistrictDTO:
    """DTO para distrito"""
    id: int
    nome: str

@dataclass
class CityDTO:
    """DTO para cidade"""
    id: int
    nome: str
    distritos: Optional[List[DistrictDTO]] = None

@dataclass
class StateDTO:
    """DTO para estado"""
    id: int
    sigla: str
    nome: str
    cidades: Optional[List[CityDTO]] = None


 