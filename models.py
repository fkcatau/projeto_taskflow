#import biblioteca
from sqlalchemy import create_engine, column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

#Base de dados - endereço
engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/taskflow')

#criar sessao
local_session = sessionmaker(bind=engine)

Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'pessoa'
