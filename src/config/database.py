from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


 
url = config('URLDB')

engine = create_engine(url)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



#!#########################    SQLITE   ############################

# url = r'sqlite:///C:\Users\jose.filho\Desktop\PY\API\app\config\test.db'

# engine = create_engine(url)

# Crie uma sessão para interagir com o banco de dados
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função de criação de uma nova sessão do banco de dados
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

