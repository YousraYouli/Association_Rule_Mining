import numpy as np
import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import numba

st.set_page_config(
    page_icon='🤖',
    page_title='Model',
    layout='wide'
)
#----------------------------------------------------------------------------------------------------------------------------------------

if "Data_loaded" not in st.session_state:
    st.session_state.Data_loaded = False
    st.session_state.View_Data = False

def disable():
    st.session_state.Data_loaded = True

st.title("Step 1 : Loading Data")

st.markdown('''
# **The EDA**

This is the **EDA** created in Streamlit using the **pandas-profiling** library.
            
For Data Visualisation
''')


# Pandas Profiling Report
def load_csv_data(path):
        try:
            df = pd.read_csv(path)
            return df
        except FileNotFoundError:
            st.error("Error: 'Groceries_dataset.csv' not found. Please ensure the file is present in the 'data' folder.")
            return None 
        
st.info('Awaiting for CSV file to be uploaded.')

if st.button('Load Data', type="primary" ,on_click=disable,  disabled=st.session_state.Data_loaded):
    st.session_state.books = load_csv_data("data\\Groceries_dataset.csv")

if st.session_state.Data_loaded:
    st.session_state.View_Data = st.toggle('View Data')
    
if st.session_state.View_Data:
    st.subheader("Basket List Data 📚")
    if st.session_state.books is not None:  
        st.write(st.session_state.books)
    else:
        st.error("An error occurred while loading data. Please try again.")

    pr = ProfileReport(st.session_state.books, explorative=True)
    st.header('**Pandas Profiling Report**')
    st_profile_report(pr)

    
st.title("Step 2 : Data Visualization")

st.title("Step 2 : Data Cleaning")
