from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

def get_session():
    uri="mysql+pymysql://root:toor@localhost/bsg_info"
    return sessionmaker(bind=create_engine(uri))()
    
    
@contextmanager
def db_read_session():
    session = get_session()
    try:
        yield session
    except:
        raise
    finally:
        session.close()

@contextmanager
def db_write_session():
    session = get_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()