import sqlalchemy as sa 
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.future.engine import Engine

from models.model_base import ModelBase 

__engine: Optional[Engine] = None 


def create_engine(sqlite: bool = False) -> Engine:
    global __engine
    
    if __engine:
        return 
    
    conn_str = "postgresql://postgres:postgres@localhost:5432/postgres"
    __engine = sa.create_engine(url=conn_str, echo=False)
    
    return __engine

def create_session() -> Session:
    global __engine
    
    if not __engine:
        create_engine()
    
    __session = sessionmaker(__engine, expire_on_commit=False, class_=Session)
    
    session: Session = __session()
    
    return session 

def create_tables() -> None: 
    global __engine 
    
    if not __engine:
        create_engine()
        
    import models.__all_models
    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)
        
    