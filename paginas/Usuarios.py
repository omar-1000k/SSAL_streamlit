import sys
import os
sys.path.append(os.getcwd())

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from api.consultas import *
import re
import pandas as pd


# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             # header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo.lower()) is not None

def dataframe_with_selections(df):
    options_builder = GridOptionsBuilder.from_dataframe(df) 
    options_builder.configure_column('catd_id',"Identificador", editable=False)
    options_builder.configure_column('nombre',"Nombre", editable=False)
    options_builder.configure_column('u_id', hide=True)
    options_builder.configure_column('appat',"Apellido Paterno", editable=False)
    options_builder.configure_column('apmat',"Apellido Materno", editable=False)
    options_builder.configure_column('estatus',"Esta Activo?", editable=False)
    options_builder.configure_column('contacto',"Contacto", editable=False)
    options_builder.configure_column('fecha_creacion',"Fecha de creación", editable=False)
    options_builder.configure_selection(selection_mode="single",use_checkbox=False)
    grid_options = options_builder.build()
    grid_return = AgGrid(df, grid_options)
    
    if len(grid_return.selected_rows)>0:
        return grid_return.selected_rows[0]
    else:
        return False


def formulario_editar(datos):
    with st.form("Modificar usuario",clear_on_submit=False):
        st.text_input("Identificador",value=datos["catd_id"],disabled=True).strip()
        st.text_input("Fecha de creación",datos['fecha_creacion'],disabled=True)
        nombre = st.text_input("*Nombre",value=datos["nombre"],key="edit_name").strip()
        appat = st.text_input("*Apellido Paterno",value=datos["appat"],key="edit_appat").strip()
        apmat = st.text_input("Apellido Materno",value=datos["apmat"],key="edit_apmat").strip()
        correo = st.text_input("*Correo",value=datos["correo"],key="edit_email").strip()
        cel = st.text_input("*Num. Contacto",value=datos["contacto"],max_chars=10,help="Número de celular o teléfono fijo",autocomplete="*",key="edit_contact")
        activo = st.checkbox("Usuario activo",value=datos["estatus"],key="edit_active")

        submitted = st.form_submit_button("Modificar")
        if submitted:
            if nombre == '' or appat == ''  or correo == '' or cel == '':
                st.warning("Los campos con * son necesarios")
            elif es_correo_valido(correo) is False:
                st.warning("Correo electrónico NO valido")
            elif not cel.isnumeric() or len(cel) < 10:
                st.warning("El contacto deben ser de 10 digitos y que sean números")
            else:
                fecha = dt.now()
                conn = st.connection("postgresql", type="sql")
                Usuario.CATD_ID = datos["catd_id"]
                Usuario.nombre = nombre
                Usuario.appat = appat
                Usuario.apmat = apmat
                Usuario.correo = correo
                Usuario.contacto = cel
                Usuario.activo = activo
                Usuario.fecha_edicion = fecha
                Usuario.fecha_creacion = datos['fecha_creacion']
                modificar_usuario(conn,Usuario)
            
def Usuario_form():
    st.title("Usuarios")
    nuevo, modificar= st.tabs(["Nuevo", "Modificar"])
    with nuevo:
        with st.form(key="form_new_user",clear_on_submit=True):
            st.text_input("*Nombre",key="new_name")
            st.text_input("*Apellido Paterno", key="new_appat")
            st.text_input("Apellido Materno", key="new_apmat")
            st.text_input("*Correo", key="new_email")
            st.text_input("*Num. Contacto", key="new_contact", max_chars=10)
            st.checkbox("Usuario activo", key="new_active")

            submitted = st.form_submit_button("Guardar")
            
        if submitted:
            fecha = dt.now()
            conn = st.connection("postgresql", type="sql")
            Usuario.nombre = (st.session_state.new_name).lower()
            Usuario.appat = st.session_state.new_appat.strip().lower()
            Usuario.apmat = st.session_state.new_apmat.strip().lower()
            Usuario.correo = st.session_state.new_email.strip().lower()
            Usuario.contacto = st.session_state.new_contact.strip()
            Usuario.activo = st.session_state.new_active
            Usuario.fecha_edicion = fecha
            Usuario.fecha_creacion = fecha
            
            if st.session_state.new_name == '' or st.session_state.new_appat == '' or st.session_state.new_email == '' or st.session_state.new_contact == '':
                st.warning("Los campos con * son necesarios")
            elif es_correo_valido(st.session_state.new_email) is False:
                st.warning("Correo electronico NO valido")
            elif not st.session_state.new_contact.isnumeric() or len(st.session_state.new_contact) < 10:
                st.warning("El contacto deben ser de 10 digitos y que sean números")
            elif existe_usr_correo(conn,st.session_state.new_email):
                st.warning(f"El correo: {st.session_state.new_email}, existe para otro usuario")
            else:
                creado = nuevo_usuario(conn,Usuario)
                if creado:
                    st.success("Usiario registrado")

    with modificar:
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                texto_buscar = st.text_input('Buscar coincidencia',value="",key="buscar_usr").strip()
                
            with col2:
                select_radio =  st.radio("Buscar por:",["Nombre", "Correo"])
        
        if texto_buscar != "":
            # Initialize connection.
            conn = st.connection("postgresql", type="sql")

            # Perform query.
            df = pd.DataFrame(consul_usuarios(conn))
            
            if select_radio=="Nombre":
                result =  df[df["nom_completo"].str.lower().str.contains(texto_buscar.lower())][["u_id","catd_id","nombre","appat", "apmat", "correo", "estatus", "contacto","fecha_creacion"]]
            else:
                result =  df[df["correo"].str.lower().str.contains(texto_buscar.lower())][["u_id","catd_id","nombre","appat", "apmat", "correo", "estatus", "contacto","fecha_creacion"]]
                
            if len(result)>0:
                seleccion = dataframe_with_selections(result)
                if seleccion:
                    formulario_editar(seleccion)
            else:
                st.warning("Sin resultados")
