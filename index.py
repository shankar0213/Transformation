import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from navigation import make_sidebar
#from navigation import hide_sidebar

import pandas as pd
import numpy as np

st.set_page_config(initial_sidebar_state="collapsed")
st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True) # To hide pages in sidebar

#
make_sidebar()
#hide_sidebar()
#st.title('Capgemini')
st.subheader('Login')
#
col1, col2 = st.columns(2)
with col1:
    with st.form("Form"): 
        name = st.text_input("User Name",type="default")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Submit",type="primary")
        if submit:  
            if name==password and name!='' and submit==True:
                result = name.title()
                st.session_state.logged_in = True
                result= "Welcome "+result
                st.success(result)
                sleep(0.5)
                st.switch_page("pages/page1.py")
                
            else:
                st.error("Incorrect Username or Password")    