import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

df = pd.DataFrame({"indice": ["a", "b", "c"],"col1": [1, 2, 3], "col2": [4, 5, 6]}).set_index("indice")

# grid_options = {
#     "columnDefs": [
#         {
#             "headerName": "col1",
#             "field": "col1",
#             "editable": True,
#         },
#         {
#             "headerName": "col2",
#             "field": "col2",
#             "editable": False,
#         },
#     ],
#     "rowSelection": 'single',
# }

options_builder = GridOptionsBuilder.from_dataframe(df) 
options_builder.configure_column('col1',"Nuevo encabezado", editable=True)
options_builder.configure_selection(selection_mode="single",use_checkbox=True)
grid_options = options_builder.build()

grid_return = AgGrid(df, grid_options)
new_df = grid_return["data"]

st.write(grid_return)

st.write(grid_return.selected_rows)

st.write(grid_return.selected_rows[0]["col1"])