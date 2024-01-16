import streamlit as st
from streamlit.connections.sql_connection import SQLConnection
import json
from sqlalchemy.sql import text
from datetime import datetime as dt



class Usuario():
    CATD_ID : str
    U_ID: str
    nombre: str
    appat: str
    apmat: str
    correo: str
    contacto:int
    activo:str
    fecha_edicion: dt.date
    fecha_creacion: dt.date


class Local():
    CATD_ID : str
    catd_cve_oiriginal: str
    CATD_Descripcion :str
    empresa_marca: str
    descipcion: str
    activo:str
    fecha_edicion: dt.date
    fecha_creacion: dt.date
    
def existe_usr_correo(conn:SQLConnection,email:str):
    sql = """ 
        SELECT catd_infoadicional ->> 'correo' correo
        FROM cat.catalogodetalle 
        where CAT_ID = 'U' and catd_infoadicional ->> 'correo' = :correo
    """
    with conn.session as session:
        result = session.execute(text(sql), params=dict(correo=email)).fetchall()
    
    if len(result)>0:
        return True
    else: 
        return False

def consul_usuarios(conn:SQLConnection):
    with conn.session as session:
        result = session.execute(text(""" 
                            SELECT 
                            CATD_ID,
                            catd_cve_oiriginal U_ID,
                            concat(catd_infoadicional ->> 'nombre',' ',catd_infoadicional ->> 'appat',' ',catd_infoadicional ->> 'apmat')nom_completo,
                            catd_infoadicional ->> 'nombre' Nombre,
                            catd_infoadicional ->> 'appat' appat,
                            catd_infoadicional ->> 'apmat' apmat,
                            catd_infoadicional ->> 'correo' correo,
                            catd_infoadicional ->> 'estatus' estatus,
                            catd_infoadicional ->> 'contacto'  Contacto,
                            catd_infoadicional ->> 'fecha_creacion' fecha_creacion 
                            FROM cat.catalogodetalle 
                            where CAT_ID = 'U' and catd_cve_oiriginal <> 'ADM' """)).fetchall()
    return result



def nuevo_usuario(conn:SQLConnection,usuario:Usuario):
    #obtner secuancia para el ID del usuario
    with conn.session as session:
        sql_sequence = """ 
        SELECT nextval('cat.seq_cat_usuario')
        """
        seq = session.execute(text(sql_sequence)).fetchall()
    
        Usuario.CATD_ID = "U-"+str(seq[0][0])
        Usuario.U_ID =  str(seq[0][0])
        indoAdi = {}
        indoAdi['nombre'] = Usuario.nombre
        indoAdi['appat'] = Usuario.appat
        indoAdi['apmat'] = Usuario.apmat
        indoAdi['correo'] = Usuario.correo
        indoAdi['contacto'] = Usuario.contacto
        indoAdi['estatus'] = Usuario.activo
        indoAdi['fecha_edicion'] = Usuario.fecha_edicion
        indoAdi['fecha_creacion'] = Usuario.fecha_creacion
        json_data = json.dumps(indoAdi,default=str)
    
        sql = " insert into ssal.cat.catalogodetalle values (:CATD_ID,:NombreUsu,:U_ID,'U',:infoadi);"

        session.execute(text(sql),params = dict(CATD_ID=Usuario.CATD_ID,U_ID=Usuario.U_ID,NombreUsu=Usuario.nombre+" "+Usuario.appat+" "+Usuario.apmat.strip(),infoadi=json_data))
        session.commit()
        session.close()

    return True


def modificar_usuario(conn:SQLConnection,usuario:Usuario):
    #obtner secuancia para el ID del usuario
    with conn.session as session:
        indoAdi = {}
        indoAdi['nombre'] = usuario.nombre
        indoAdi['appat'] = usuario.appat
        indoAdi['apmat'] = usuario.apmat
        indoAdi['correo'] = usuario.correo
        indoAdi['contacto'] = usuario.contacto
        indoAdi['estatus'] = usuario.activo
        indoAdi['fecha_edicion'] = usuario.fecha_edicion
        indoAdi['fecha_creacion'] = usuario.fecha_creacion
        json_data = json.dumps(indoAdi,default=str)
    
        sql = """ update ssal.cat.catalogodetalle 
        set catd_descripcion = :NombreCompleto,
        catd_infoadicional = :infoadi 
        where CATD_ID = :CATD_ID """

        session.execute(text(sql),params = dict(CATD_ID=Usuario.CATD_ID,NombreCompleto=Usuario.nombre+" "+Usuario.appat+" "+Usuario.apmat.strip(),infoadi=json_data))
        session.commit()
        session.close()
        st.success("Usuario actualizado")


def existe_local(num_local:str):
    conn = st.connection("postgresql", type="sql")
    
    sql = """ 
        SELECT 
        CATD_ID
        FROM cat.catalogodetalle 
        where CATD_ID = :local
    """
    with conn.session as session:
        result = session.execute(text(sql), params=dict(local=num_local)).fetchall()
    
    session.close()
    if len(result)>0:
        return True
    else: 
        return False



def nuevo_local(local:Local):
    #obtner secuancia para el ID del usuario
    conn = st.connection("postgresql", type="sql")
    with conn.session as session:
        
        indoAdi = {}
        indoAdi['empresa_marca'] = local.empresa_marca
        indoAdi['descipcion'] = local.descipcion
        indoAdi['activo'] = local.activo
        indoAdi['fecha_edicion'] = local.fecha_edicion
        indoAdi['fecha_creacion'] = local.fecha_creacion
        json_data = json.dumps(indoAdi,default=str)
    
        sql = " insert into ssal.cat.catalogodetalle values (:CATD_ID,:CATD_Descripcion,:catd_cve_oiriginal,'L',:infoadi);"

        session.execute(text(sql),params = dict(CATD_ID=local.CATD_ID, CATD_Descripcion=local.CATD_Descripcion,catd_cve_oiriginal=local.catd_cve_oiriginal,infoadi=json_data))
        session.commit()
        session.close()

    return True


def consul_locales():
    conn = st.connection("postgresql", type="sql")
    with conn.session as session:
        result = session.execute(text(""" 
                            SELECT 
                            CATD_ID,
                            catd_descripcion,
                            catd_cve_oiriginal,
                            catd_infoadicional ->> 'empresa_marca' empresa_marca,
                            catd_infoadicional ->> 'descipcion' descipcion,
                            catd_infoadicional ->> 'activo' activo,
                            catd_infoadicional ->> 'fecha_creacion' fecha_creacion 
                            FROM cat.catalogodetalle 
                            where CAT_ID = 'L' """)).fetchall()
    return result


def modificar_local(local:Local):
    conn = st.connection("postgresql", type="sql")
    with conn.session as session:
        indoAdi = {}
        indoAdi['empresa_marca'] = local.empresa_marca
        indoAdi['descipcion'] = local.descipcion
        indoAdi['activo'] = local.activo
        indoAdi['fecha_edicion'] = local.fecha_edicion
        indoAdi['fecha_creacion'] = local.fecha_creacion
        json_data = json.dumps(indoAdi,default=str)
    
        sql = """ update ssal.cat.catalogodetalle 
        set catd_descripcion = :CATD_Descripcion,
        catd_infoadicional = :infoadi 
        where CATD_ID = :CATD_ID """

        session.execute(text(sql),params = dict(CATD_ID=local.CATD_ID, CATD_Descripcion=local.CATD_Descripcion,infoadi=json_data))
        session.commit()
        session.close()
        