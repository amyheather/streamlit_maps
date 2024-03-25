import json
from kailo_beewell_dashboard.map import choose_topic
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Streamlit maps', page_icon='🌍')

# Title and method description
st.title('Plotly express map')
st.markdown('''
**Interactive** map. Good performance.''')

# Import data to session state
if 'scores_rag' not in st.session_state:
    st.session_state.scores_rag = pd.read_csv(
        'data/survey_data/standard_area_aggregate_scores_rag.csv')
if 'geojson_nd' not in st.session_state:
    f = open('data/geojson/combined_nd.geojson')
    st.session_state.geojson_nd = json.load(f)

# As we play around this one, import it from session state
df_scores = st.session_state.scores_rag

# Create selectbox and get chosen topic
chosen_variable_lab = choose_topic(df_scores)

# Filter to chosen topic then filter to only used column (helps map speed)
chosen_result = df_scores[df_scores['variable_lab'] == chosen_variable_lab]
msoa_rag = chosen_result[['msoa', 'mean']]

#######
# Map #
#######

# Replace NaN with "n<10", and use full label names for other categories
msoa_rag['rag'] = msoa_rag['rag'].map({
    'below': 'Below average',
    'average': 'Average',
    'above': 'Above average',
    np.nan: 'n<10'})

# Create map
fig = px.choropleth_mapbox(
    msoa_rag,
    geojson=st.session_state.geojson_nd,
    locations='msoa',
    featureidkey="properties.MSOA11NM",
    # Colour rules
    color='rag',
    color_discrete_map={'Below average': '#FFB3B3',
                        'Average': '#FFDFA6',
                        'Above average': '#7DD27D',
                        'n<10': '#F6FAFF'},
    opacity=0.75,
    # Base map stryle
    mapbox_style='carto-positron',
    # Positioning of map on load
    center={'lat': 50.955, 'lon': -4.1},
    zoom=8.4,
    labels={'rag': 'Result'},
    # Control legend order
    category_orders={
        'rag': ['Below average', 'Average', 'Above average', 'n<10']})

fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
st.plotly_chart(fig)