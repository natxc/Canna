import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction import FeatureHasher
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist 
from sklearn.neighbors import NearestNeighbors
import altair as alt 

# Dashboard container size
def set_block_container_style():
    # max_width_str = f"max-width: 2000px"
    st.markdown(
        f"""
<style>
    .element-container markdown-text-container{{
        width: 1500 px;
    }}
    .block-container{{
        width: 1500 px;
        padding-top: 5 rem;
        padding-right: 1 rem;
        padding-left: 1 rem;
        padding-bottom: 10 rem;
    }}
</style>
"""
        # unsafe_allow_html=True,
    )

# Intro
st.title("Cannabis Strain Picker by Effect & Flavor!")
# load raw data & display
@st.cache  
# @st.cache(allow_output_mutation=True)
def load_data(nrows):
    data = pd.read_csv("cannabis.csv", nrows=nrows)
    data = data.fillna("None")
    return data 

# data_load_state = st.text('Loading data...')
data = load_data(10000)
# data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
# 'data', data

# Effects
from canna_recommend_system import total_effects
effect_selection = st.sidebar.selectbox('Strain Effect', total_effects)
if effect_selection == "All Effects":
    effect_filter = pd.DataFrame(data)
else:
    effect_filter = pd.DataFrame(data[data['Effects'].str.contains(effect_selection)])
# st.write(effect_filter)

# Flavor 
from canna_recommend_system import total_flavor
# 'total_flavor', total_flavor

flavor_selection = st.sidebar.selectbox('Strain Flavor',total_flavor)
if flavor_selection == "All Flavors":
    flavor_filter = pd.DataFrame(data) 
else:
    flavor_filter = pd.DataFrame(data[data['Flavor'].str.contains(flavor_selection)])
# st.write(flavor_filter)

# Rating
rating_slider = st.sidebar.slider('Filter by Rating', 0,5)
rating_filter = pd.DataFrame(data[data['Rating'] >= int(rating_slider)])


# Result DataFrame

st.write('## Best Matched Strains by Selection')
match_df = pd.DataFrame.merge(effect_filter, flavor_filter, on='Strain', how='inner', left_index=False, right_index=False)
final_df = pd.DataFrame.merge(match_df, rating_filter, how='inner', on='Strain', left_index=False, right_index=False)
# match_df = match_df[match_df['Flavor'].str.contains(flavor_selection)]
# match_df = pd.DataFrame(flavor_filter,effect_filter)
clean_df = final_df.drop(columns=['Type_x','Rating_x','Effects_x','Flavor_x','Description_x','Type_y','Rating_y','Effects_y','Flavor_y','Description_y'])
st.write(clean_df) 