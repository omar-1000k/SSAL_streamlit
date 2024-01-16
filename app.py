import streamlit as st
from streamlit_option_menu import option_menu
from paginas.Usuarios import Usuario_form
from paginas.Locales import Local_form


def principal():

    with st.sidebar:
        choose = option_menu("SSAL", ["Usuario","Local"],
                            icons=['person-plus','shop-window'],
                            menu_icon="house", default_index=0,
                            styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "black", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#DFDBDA"},
            "nav-link-selected": {"background-color": "red"},
        }
        )

    if choose == "Usuario":
        Usuario_form()
    if choose == "Local":
        Local_form()

principal()