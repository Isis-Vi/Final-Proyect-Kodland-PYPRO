from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///carbon_footprint.db', echo=True)
Base = declarative_base()

#Crear la tabla de la base de datos
class CarbonFootPrint(Base):
    __tablename__ = 'carbon_footprint'

    user_id = Column(String,primary_key=True, nullable=False)
    km_carro = Column(Float, nullable=False)
    kwh = Column(Float, nullable=False)
    plasticos = Column(Integer, nullable=False)
    carne = Column(String, nullable=False)
    huella_total = Column(Float, nullable=False)
Base.metadata.create_all(engine)

# Obtener la conexión (Permite insertar,eliminar,actualizar datos de la base de datos)
def get_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# Para insertar datos en la base de datos
def insert_row(user_id, km_carro, kwh, plasticos, carne, huella_total,engine):
    nuevo_registro_db = CarbonFootPrint(
        user_id=user_id,
        km_carro = km_carro,
        kwh = kwh,
        carne = carne,
        plasticos = plasticos,
        huella_total = huella_total
    )
    session = get_session(engine)
    session.add(nuevo_registro_db)
    session.commit()
    return True

# Para acceder a la base de datos (confirmar si hay existente)
def has_carbonfootprint(user_id,engine)-> bool:
    session = get_session(engine)
    try:
        response = session.query(CarbonFootPrint).filter_by(user_id=user_id).all()
        if len(response) > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Erorr al obtener registros: {e}")
    finally:
        session.close()

#Pare re-escribir los resultados bajo la misma ID
def delete_carbon_foot_print(user_id,engine):
    session = get_session(engine)
    try:
        # Verificar si el usuario tiene registros
        old_carbon_foot_print = session.query(CarbonFootPrint).filter_by(user_id=user_id).all()
        if len(old_carbon_foot_print) > 0:
            session.delete(old_carbon_foot_print[0])
            session.commit()
            return True
        else:
            print(f"No se encontró ningún registro par el usuario {user_id}.")
            return False
    except Exception as e:
        session.rollback() # Revertir los cambios en caso de un error
        print(f"Error al eliinar la huella de carbono vieja {e}")
        return False
    finally:
        session.close()

#Para acceder a la columna huella total de la db.
def get_current_carbon_foot_print(user_id,engine):
    session = get_session(engine)
    try:
        current_carbon_foot_print = session.query(CarbonFootPrint).filter_by(user_id=user_id).all()
        huella_usuario = current_carbon_foot_print[0].huella_total
        return huella_usuario
    except Exception as e:
        print(f"Erorr al obtener registros: {e}")
    finally:
        session.close()

#Para acceder a las otras columnas
def get_current_km_carro(user_id,engine):
    session = get_session(engine)
    try:
        current_km_carro = session.query(CarbonFootPrint).filter_by(user_id=user_id).all()
        carro_usuario = current_km_carro[0].km_carro
        return carro_usuario
    except Exception as e:
        print(f"Erorr al obtener registros: {e}")
    finally:
        session.close()

    #KwH
def get_current_kwh(user_id,engine):
    session = get_session(engine)
    try:
        current_kwh = session.query(CarbonFootPrint).filter_by(user_id=user_id).all()
        kwh_usuario = current_kwh[0].kwh
        return kwh_usuario
    except Exception as e:
        print(f"Erorr al obtener registros: {e}")
    finally:
        session.close()

    #Carne
def get_current_carne(user_id,engine):
    session = get_session(engine)
    try:
        current_carne = session.query(CarbonFootPrint).filter_by(user_id=user_id).all()
        carne_usuario = current_carne[0].carne
        return carne_usuario
    except Exception as e:
        print(f"Erorr al obtener registros: {e}")
    finally:
        session.close()

    #Plásticos
def get_current_plastico(user_id,engine):
    session = get_session(engine)
    try:
        current_plasticos = session.query(CarbonFootPrint).filter_by(user_id=user_id).all()
        plastico_usuario = current_plasticos[0].plasticos
        return plastico_usuario
    except Exception as e:
        print(f"Erorr al obtener registros: {e}")
    finally:
        session.close()




