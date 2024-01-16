import streamlit as st
import pandas as pd
from api.consultas import *
from datetime import datetime as dt
from st_aggrid import AgGrid, GridOptionsBuilder

def dataframe_with_selections(df):
    options_builder = GridOptionsBuilder.from_dataframe(df) 
    options_builder.configure_column('catd_descripcion',"Número de local", editable=False)
    options_builder.configure_column('empresa_marca',"Empresa/Marca", editable=False)
    options_builder.configure_column('catd_id', hide=True)
    options_builder.configure_column('catd_cve_oiriginal', hide=True)
    options_builder.configure_column('descipcion',"Descripcion", editable=False)
    options_builder.configure_column('activo',"Esta Activo?", editable=False)
    options_builder.configure_column('fecha_creacion',"Fecha de creación", editable=False)
    options_builder.configure_selection(selection_mode="single",use_checkbox=False)
    grid_options = options_builder.build()
    grid_return = AgGrid(df, grid_options)
    
    if len(grid_return.selected_rows)>0:
        return grid_return.selected_rows[0]
    else:
        return False

def formulario_editar(datos:Local):
    with st.form("Modificar local",clear_on_submit=False):
        st.text_input("Identificador",value=datos["catd_id"],disabled=True,key="edit_catd_id_local").strip()
        st.text_input("*Num de local",key="edit_num_local")
        st.text_input("*Empresa/Marca", key="edit_marca")
        st.text_input("Ubicación/Descripción", key="edit_local_desc")
        st.checkbox("Local activo", key="edit_local_active")

        submitted = st.form_submit_button("Modificar")
        if submitted:
            if st.session_state.edit_num_local == '' or st.session_state.edit_marca == '':
                st.warning("Los campos con * son necesarios")
            elif existe_local(st.session_state.edit_num_local):
                st.warning(f"El número de local: {st.session_state.edit_num_local}, ya existe")
            else:
                fecha = dt.now()
                Local.CATD_ID = datos["catd_id"]
                Local.CATD_Descripcion = st.session_state.edit_num_local.strip().lower()
                Local.catd_cve_oiriginal = st.session_state.edit_num_local.strip().lower()
                Local.empresa_marca = st.session_state.edit_marca.strip().lower()
                Local.descipcion = st.session_state.edit_local_desc.strip().lower()
                Local.activo = st.session_state.edit_local_active
                Local.fecha_edicion = fecha
                Local.fecha_creacion = datos['fecha_creacion']
                modificar_local(Local)
                st.success("Usuario actualizado")
                
def Local_form():
    st.title("Locales")
    nuevo, modificar= st.tabs(["Nuevo", "Modificar"])
    with nuevo:
        with st.form(key="form_new_local",clear_on_submit=True):
            st.text_input("*Num de local",key="new_num_local")
            st.text_input("*Empresa/Marca", key="new_marca")
            st.text_input("Ubicación/Descripción", key="new_local_desc")
            st.checkbox("Local activo", key="new_local_active")

            submitted = st.form_submit_button("Guardar")
            
        if submitted:
            fecha = dt.now()
            Local.CATD_ID = 'L-'+st.session_state.new_num_local.strip().lower()
            Local.CATD_Descripcion = st.session_state.new_num_local.strip().lower()
            Local.catd_cve_oiriginal = st.session_state.new_num_local.strip().lower()
            Local.empresa_marca = st.session_state.new_marca.strip().lower()
            Local.descipcion = st.session_state.new_local_desc.strip().lower()
            Local.activo = st.session_state.new_local_active
            Local.fecha_edicion = fecha
            Local.fecha_creacion = fecha
            
            
            if st.session_state.new_num_local == '' or st.session_state.new_marca == '':
                st.warning("Los campos con * son necesarios")
            elif existe_local(Local.CATD_ID):
                st.warning(f"El número de local: {st.session_state.new_num_local}, ya existe")
            else:
                creado = nuevo_local(Local)
                if creado:
                    st.success("Local registrado")

    with modificar:
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                texto_buscar = st.text_input('Buscar coincidencia',value="",key="buscar_local").strip()
                
            with col2:
                select_radio =  st.radio("Buscar por:",["Núm Local", "Empresa/Marca"])
        
        if texto_buscar != "":
            # Perform query.
            df = pd.DataFrame(consul_locales())
            
            if select_radio=="Núm Local":
                result =  df[df["catd_cve_oiriginal"].str.lower().str.contains(texto_buscar.lower())][["catd_id","catd_descripcion","catd_cve_oiriginal","empresa_marca", "descipcion", "activo", "fecha_creacion"]]
            else:
                result =  df[df["empresa_marca"].str.lower().str.contains(texto_buscar.lower())][["catd_id","catd_descripcion","catd_cve_oiriginal","empresa_marca", "descipcion", "activo", "fecha_creacion"]]
                
            if len(result)>0:
                seleccion = dataframe_with_selections(result)
                if seleccion:
                    formulario_editar(seleccion)
            else:
                st.warning("Sin resultados")