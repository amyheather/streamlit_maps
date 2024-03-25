import streamlit as st

st.set_page_config(page_title='Streamlit maps', page_icon='🌍')

st.title('Streamlit maps')
st.markdown('''
This app and repository demonstrates a few options for producing maps
within streamlit apps. You can navigate to these using the sidebar:
* **Folium** - interactive, poor performance
* **Plotly express** - interactive, good performance''')