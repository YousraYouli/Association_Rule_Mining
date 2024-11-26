import numpy as np
import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import numba
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


st.set_page_config(
    page_icon='🤖',
    page_title='Model',
    layout='wide'
)
#----------------------------------------------------------------------------------------------------------------------------------------

if "Data_loaded" not in st.session_state:
    st.session_state.Data_loaded = False
    st.session_state.View_Data = False
    st.session_state.Results1 = False

def disable():
    st.session_state.Data_loaded = True
def Res1():
    st.session_state.Results1 = True

#----------------------------------------------------------------------------------------------------------------------------------------
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
        
#----------------------------------------------------------------------------------------------------------------------------------------

st.info('Awaiting for CSV file to be uploaded.')

if st.button('Load Data', type="primary" ,on_click=disable,  disabled=st.session_state.Data_loaded):
    st.session_state.books = load_csv_data("data\\Groceries_dataset.csv")
    st.session_state.cleaned_basket_data = load_csv_data("data\\cleaned_basket_data.csv")
    
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

#----------------------------------------------------------------------------------------------------------------------------------------

st.title("Step 2 : Data Visualization")
if st.session_state.Data_loaded: 

    st.markdown(
    """
### Please choose from the :orange[SideBar] which :orange[Statistic] you wanna check 
"""
)

    # Summary statistics
    st.write("### Summary Statistics:")
    st.write(st.session_state.books.describe())

    # Visualizations
    st.write("## Visualizations")

    # Item Popularity
    st.write("### Item Popularity")
    item_counts = st.session_state.books['itemDescription'].value_counts()
    plt.bar(item_counts.index[:10], item_counts.values[:10])
    plt.xlabel('Item Description')
    plt.ylabel('Frequency')
    plt.title('Top 10 Most Popular Items')
    plt.xticks(rotation=45)
    st.pyplot()

    # Check for missing values
    st.write("Missing Values:")
    st.write(st.session_state.books.isnull().sum())
    # Visualize missing values using a heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(st.session_state.books.isnull(), cmap='viridis')
    plt.title("Missing Values Heatmap")
    st.pyplot()

    # Box plot to visualize outliers
    st.write("Box Plots to Detect Outliers:")
    for column in st.session_state.books.select_dtypes(include=['float64', 'int64']).columns:
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=st.session_state.books[column])
        plt.title(f"Box Plot for {column}")
        st.pyplot()

    # Word Cloud
    st.write("### Word Cloud of Items")
    text = " ".join(review for review in st.session_state.books['itemDescription'])
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110).generate(text)
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation="bilinear") 

    plt.axis("off")
    plt.show() 

    # Transaction Length Distribution
    st.write("### Transaction Length Distribution")
    plt.hist(st.session_state.books.groupby('Member_number')['itemDescription'].count(), bins=20)
    plt.xlabel('Number of Items per Transaction')
    plt.ylabel('Frequency')
    plt.title('Transaction Length Distribution')
    st.pyplot()


  
#----------------------------------------------------------------------------------------------------------------------------------------


st.title("Step 3 : Data Cleaning")
if st.session_state.Data_loaded: 
    st.write("## the hot-encoding dataset ")
    code_p1 = ('''
 
            # Prétraitement: Grouper les articles par chaque transaction
            transactions = st.session_state.books.groupby('Member_number')['itemDescription'].apply(list)
            transactions
               
            # Convertir les transactions au format One-Hot Encoding
            encoder = TransactionEncoder()
            pred = encoder.fit_transform(transactions)
            df = pd.DataFrame(pred,columns = encoder.columns_)
               
            #Extracting the results as csv for use in Excel
            df.to_csv("cleaned_basket_data.csv")

            ''')

    st.code(code_p1, language='python')

    st.button("Excute the code and show results", on_click=Res1, disabled=st.session_state.Results1)

if st.session_state.Results1:

    st.subheader('Generated Dataframe from the previous treatment')
    st.dataframe(st.session_state.cleaned_basket_data, use_container_width=True)
