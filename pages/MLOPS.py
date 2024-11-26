import streamlit as st
import reveal_slides as rs

st.set_page_config(
    page_icon='👨‍💻',
    page_title='MLOps',
    layout='wide'
)

sample_markdown = r'''
# MLOps


---
## What is MLOps?

It stands for Machine Learning Operations.\
As it is a part of Machine Learning engineering,
it focuses on simplifying the production, maintenance and monetization of ML models,
the process MLOps often comprises data scientists, devops engineers and IT.


'''

currState = rs.slides(sample_markdown, 
                    height=720, 
                    # theme='blood', 
                    initial_state={
                                    "indexh": 0, 
                                    "indexv": 0, 
                                    "indexf": -1, 
                                    "paused": False, 
                                    "overview": False 
                                    }, 
                    markdown_props={"data-separator-vertical":"^--$"}, 
                    key="foo")
