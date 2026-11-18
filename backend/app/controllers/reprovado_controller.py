from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reprovado import Reprovado
from app.models.user import User
from app.schemas.reprovado import ReprovadoCreate, ReprovadoResponse

router = APIRouter(
    prefix='/reprovados',
    tags=['Reprovados']
)


@router.post(
    '/',
    response_model=ReprovadoResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_reprovado(
    dados: ReprovadoCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    agora = datetime.now()

    usuario = db.query(User).filter(User.cpf == dados.cpf).first()

    reprovado = db.query(Reprovado).filter(Reprovado.cpf == dados.cpf).first()

    if reprovado:

        reprovado.nome = dados.nome
        reprovado.data_ultima_solicitacao = dados.data_ultima_solicitacao or agora
        reprovado.data_reprovacao = agora
        if dados.data_ultimo_contato:
            reprovado.data_ultimo_contato = dados.data_ultimo_contato
        if usuario:
            reprovado.usuario_id = usuario.id
        response.status_code = status.HTTP_200_OK
    else:
        reprovado = Reprovado(
            usuario_id=usuario.id if usuario else None,
            nome=dados.nome,
            cpf=dados.cpf,
            data_ultima_solicitacao=dados.data_ultima_solicitacao or agora,
            data_reprovacao=agora,
            data_ultimo_contato=dados.data_ultimo_contato
        )
        db.add(reprovado)

    db.commit()
    db.refresh(reprovado)
    return reprovado


@router.get(
    '/cpf/{cpf}',
    response_model=ReprovadoResponse
)
def reconhecer_reprovado(
    cpf: str,
    db: Session = Depends(get_db)
):

    reprovado = db.query(Reprovado).filter(Reprovado.cpf == cpf).first()

    if not reprovado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='CPF não consta como reprovado.'
        )

    return reprovado


@router.get(
    '/',
    response_model=list[ReprovadoResponse]
)
def listar_reprovados(
    db: Session = Depends(get_db)
):
    return db.query(Reprovado).order_by(Reprovado.data_reprovacao.desc()).all()


@router.patch(
    '/{reprovado_id}/contato',
    response_model=ReprovadoResponse
)
def registrar_contato(
    reprovado_id: int,
    db: Session = Depends(get_db)
):

    reprovado = db.query(Reprovado).filter(Reprovado.id == reprovado_id).first()

    if not reprovado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Reprovado não encontrado.'
        )

    reprovado.data_ultimo_contato = datetime.now()
    db.commit()
    db.refresh(reprovado)
    return reprovado
