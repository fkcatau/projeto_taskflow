from sqlalchemy import create_engine, Column, Integer, String, Date, Time, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

url = 'mysql+pymysql://root:senaisp@localhost:3306/taskflow'

if not database_exists(url):
    create_database(url)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

atividade_recurso = Table(
    'atividade_recurso',
    Base.metadata,
    Column('atividade_id', Integer, ForeignKey('atividade.id', ondelete='CASCADE'), primary_key=True),
    Column('recurso_id', Integer, ForeignKey('recurso.id', ondelete='CASCADE'), primary_key=True)
)


class Pessoa(Base):
    __tablename__ = 'pessoa'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    data_nascimento = Column(Date, nullable=False)
    senha = Column(String(255), nullable=False)
    papel = Column(String(100), default='usuario', nullable=False)

    atividades = relationship("Atividade", back_populates="responsavel")

    def __repr__(self):
        return f'<Pessoa {self.nome}>'


class Tipo(Base):
    __tablename__ = 'tipo'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    desc = Column(String(255), nullable=False)

    atividades = relationship("Atividade", back_populates="tipo")


class Recurso(Base):
    __tablename__ = 'recurso'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=False)

    atividades = relationship("Atividade", secondary=atividade_recurso, back_populates="recursos")


class Atividade(Base):
    __tablename__ = 'atividade'
    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)

    pessoa_id = Column(Integer, ForeignKey('pessoa.id'), nullable=False)
    tipo_id = Column(Integer, ForeignKey('tipo.id'), nullable=False)

    responsavel = relationship("Pessoa", back_populates="atividades")
    tipo = relationship("Tipo", back_populates="atividades")
    recursos = relationship("Recurso", secondary=atividade_recurso, back_populates="atividades")


def init_db():
    Base.metadata.create_all(bind=engine)
