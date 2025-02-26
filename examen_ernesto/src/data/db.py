from sqlmodel import create_engine, SQLModel, Session
from src.models.compra import Compra

db_user: str = "quevedo"  
db_password: str =  "1234"
db_server: str = "localhost" 
db_port: int = 3306  
db_name: str = "comprasdb"  

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Compra(producto="Pimiento", tipo="verdura", precio=3))
        session.add(Compra(producto="Manzana", tipo="Fruta", precio=2))
        session.add(Compra(producto="Yogurt", tipo="Postres", precio=1))
        session.commit()
        #session.refresh_all()