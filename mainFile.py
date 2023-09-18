import streamlit as st
# import xlsxwriter
# import io
import pyodbc
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid import GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode
# import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader


sampleSqlQuery = """ SELECT T1.[ItemCode], T0.[ItemName],T1.[WhsCode], T2.[WhsName], T1.[OnHand]  
  FROM OITM T0 INNER JOIN OITW T1 ON T0.[ItemCode] = T1.[ItemCode]  
  INNER JOIN OWHS T2 ON T1.[WhsCode] = T2.[WhsCode]  
  WHERE T1.[OnHand]<>0 
  ORDER BY T1.[WhsCode],T1.[ItemCode]"""

# ----------------- ESTABLISHING db connection
server = '10.10.10.100'
database = 'LB'
username = 'ayman'
password = 'admin@1234'
connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
connection = pyodbc.connect(connection_string)
# ----------------- ESTABLISHING db connection


# This Creates the Table For us  , line 115
def create_aggrid(data, multicolumn):
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_default_column(
        min_column_width=6, enablePivot=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_column(multicolumn, headerCheckboxSelection=True)
    gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
    gridOptions = gb.build()

    response = AgGrid(
        data,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        height=600,
    )
    return response

# 1 Make the query RUN with the Connection above and Get the Dataframe
whs_stock = pd.read_sql(sampleSqlQuery, connection)
# 2 Show this DataFrame In the Page 
response = create_aggrid(whs_stock,'ItemCode')


