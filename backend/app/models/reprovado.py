from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.database import Base


class Reprovado(Base):
    __tablename__ = 'reprovados'

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)

    nome = Column(String(100), nullable=False)

    cpf = Column(String(11), unique=True, nullable=False, index=True)

    data_ultima_solicitacao = Column(DateTime, nullable=False, default=datetime.now)
    data_reprovacao = Column(DateTime, nullable=False, default=datetime.now)
    data_ultimo_contato = Column(DateTime, nullable=True)
