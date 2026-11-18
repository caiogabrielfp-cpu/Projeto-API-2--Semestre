from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field



class ReprovadoCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    cpf: str = Field(pattern=r'^\d{11}$', description='Somente os 11 números')
    data_ultima_solicitacao: Optional[datetime] = None  
    data_ultimo_contato: Optional[datetime] = None


class ReprovadoResponse(BaseModel):
    id: int
    usuario_id: Optional[int]
    nome: str
    cpf: str
    data_ultima_solicitacao: datetime
    data_reprovacao: datetime
    data_ultimo_contato: Optional[datetime]

    class Config:
        from_attributes = True
