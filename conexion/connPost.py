from os import abort
from sqlalchemy import create_engine, types, text
import psycopg2
import abort as abort

def AbreConn():
    try:
        server = '192.168.56.103'
        engine = create_engine('postgresql+psycopg2://usr_ssal:Ss4l2023$@%s/ssal' % server)
        engine.connect()
        return engine
    except Exception as e:
        mensaje = 'Error de conexión connPost' + str(e)
        try:
            engine.dispose()
        except Exception as e:
            pass
        finally:
            abort.abort_post(engine,mensaje)

def EjecutaSQL(engine, sql):
    try:
        result = engine.execute(text(sql))
        data = result.fetchall()
        return data
    except Exception as e:
        return False

def EjecutaDDL(engine,sql):
    try:
        result = engine.execute(text(sql)).execution_options(autocommit=True)
        
        return result
    except Exception as e:
        print ('Error de connPost de BD: '+ str(e))
        return False

def CierraConn(engine):
    try:
        engine.dispose()
    except Exception as e:
        print('Error al cerrar la conexion' + str(e))