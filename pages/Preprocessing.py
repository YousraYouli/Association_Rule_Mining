import streamlit as st
import pandas as pd
import pickle


st.set_page_config(
    page_icon='📊',
    page_title='Data',
    layout='wide'
)

#------------------------------------------------------------------------------------------------------------------------------------
if "Data_loaded" not in st.session_state:
    st.session_state.Data_loaded = False
    st.session_state.View_Data = False
    st.session_state.Results1 = False
    st.session_state.Results2 = False
    st.session_state.Results3 = False

@st.cache_data
def load_model(path):
    loaded_model = pickle.load(open(path, 'rb'))
    return loaded_model

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    return data

def disable():
    st.session_state.Data_loaded = True

def Res1():
    st.session_state.Results1 = True

def Res2():
    st.session_state.Results2 = True


def Res3():
    st.session_state.Results3 = True


#------------------------------------------------------------------------------------------------------------------------------------------------

st.title("Loading Data")
st.subheader("The first step would be to load our data")



if st.button("Load Data", type="primary", on_click=disable, disabled=st.session_state.Data_loaded):
    st.session_state.Data_loaded = True
    st.session_state.books = load_data("data\\Groceries_dataset.csv")
   
if st.session_state.Data_loaded:
    code_p1 = ('''
            # The following instruction from the pandas library as pd is used to load a csv file
            Data = pd.read_csv("csvFileName.csv")
            ''')
    st.code(code_p1, language='python')
    st.session_state.View_Data = st.toggle('View Data')

if st.session_state.View_Data:
    st.subheader("Basket List Data 📚")
    st.write(st.session_state.books)

st.divider() #----------------------------------------------------------------------------------------------------------------------------------

if st.session_state.Data_loaded:
    st.title("Exploratory Data Analysis")
    st.subheader("Next let's explore our data a bit")
    st.markdown(
    """
### Please choose from the :orange[SideBar] which :orange[Statistic] you wanna check 
"""
)
    with st.sidebar:
        op1 = st.checkbox("Basket Distrubtion")
       
if st.session_state.Data_loaded:

    if op1:
        st.subheader('Ratings Distrubtion⭐')
        rating = st.slider('Choose a minimum rating', 0, 10, 0)
        st.write("higher or equal to ", rating, ' out of 10')
        st.bar_chart(st.session_state.ratings.drop(st.session_state.ratings.loc[st.session_state.ratings['Book-Rating']<rating].index)['Book-Rating'].value_counts())
   
    st.divider()

    #---------------------------------------------------------------------------------------------------------------------------------------------
st.title("Data Pre-Processing")

st.subheader("Using the pandas library and excuting the following code will merge the necessary dataframes, remove unnecessary features, irrelevant rows and extracting the results for use in the next step ")

code_p1 = ('''
            #Feature Selection from the books Dataframe
            books.drop(['Image-URL-S', 'Image-URL-M','Image-URL-L','Publisher','Year-Of-Publication','Book-Author'], axis=1, inplace=True)

            #Merging the ratings and books DataFrames
            df = pd.merge(books, ratings, on="ISBN")

            #Order the Dataframe based on user-ID in Ascending order
            df.sort_values(by=['User-ID'],inplace=True)

            #Droping all rows containing raitings lower than 5
            df.drop(df.loc[df['Book-Rating']<5].index, inplace=True)

            #Extracting the results as csv for use in Excel
            df.to_csv("users_ratings_books.csv")

            ''')

st.code(code_p1, language='python')

st.button("Excute the code and show results", on_click=Res1, disabled=st.session_state.Results1)
