import json
from kailo_beewell_dashboard.map import choose_topic
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

fig = px.choropleth_mapbox(
    msoa_rag,
    geojson=st.session_state.geojson_nd,
    locations='msoa',
    color='mean',
    featureidkey="properties.MSOA11NM",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    center={'lat': 50.955, 'lon': -4.075},
    zoom=8,
    labels={'val': 'value'})

fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

st.plotly_chart(fig)