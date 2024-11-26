import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_icon='🤖',
    page_title='Model',
    layout='wide'
)

def load_csv_data(path):
        try:
            df = pd.read_csv(path)
            return df
        except FileNotFoundError:
            st.error("Error: 'Groceries_dataset.csv' not found. Please ensure the file is present in the 'data' folder.")
            return None 
st.session_state.books = load_csv_data("data\\cleaned_basket_data.csv")
#----------------------------------------------------------------------------------------------------------------------------------------
st.sidebar.header('User Input Features')

st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/penguins_example.csv)
""")


items_list = st.session_state.books.columns.tolist()

uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
    st.write(input_df)
else:
   
    options = st.multiselect('Choose an item 📚:' , items_list)

    st.write('The recommended books for you:')
    recommendations = []
    options.sort()

    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
   
   
#---------------------------------------------------------------------------------------------------------------------------------
@st.cache_data
def load_model(path):
    loaded_model = pickle.load(open(path, 'rb'))
    return loaded_model

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    return data

# Apriori_mod = load_model("data\\apyiori_model.ob")
# Book_list = load_model('data\\Books_List.ob')
Apriori_mod = pickle.load(open("data\\apyiori_model.ob", 'rb'))
st.write('The recommended books for you:')

# Access the model directly and make predictions
# prediction = Apriori_mod.predict(input_df)
# prediction_proba = Apriori_mod.predict_proba(input_df)
# Reads in saved classification model
# load_clf = pickle.load(open('penguins_clf.pkl', 'rb'))


st.subheader('Predictions')
# penguins_species = np.array(['Adelie','Chinstrap','Gentoo'])
# st.write(prediction)
# 
st.subheader('Prediction Probability')
# st.write(prediction_proba)

