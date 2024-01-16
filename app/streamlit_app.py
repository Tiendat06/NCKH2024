import streamlit as st
import requests
from streamlit import session_state

session_state['flask'] = 'http://localhost:5000';

st.title("Hello from Streamlit!")
st.write("This is a Streamlit app running within a Flask app.")


st.write(f'''<h1>
<a target="_self"
href="http://localhost:5000">Go back homepage</a></h1>''',
unsafe_allow_html=True)