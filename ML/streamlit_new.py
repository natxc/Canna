import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction import FeatureHasher
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist 
from sklearn.neighbors import NearestNeighbors
import altair as alt 
import base64
from sklearn import preprocessing 
import os, urllib
from conjointanalysis_def import Machine_Learning



# # Dashboard container size
def _max_width_():
    max_width_str = f"max-width: 1200px;"
    st.markdown(
        f""" 
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }} 
    </style>    
    """,
        unsafe_allow_html=True,
    )



#Build APP
_max_width_() 

def main():
    # Render the readme as markdown using st.markdown.

    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose the app mode",
        ["Show raw data", "Interactive filters", "Run the app","Show source code"])
    if app_mode == "Show raw data":
        raw_data(data)
    elif app_mode == "Interactive filters":
        filter_data(data)   
    elif app_mode == "Run the app":
        run_the_app()
    # elif app_mode == "Show the source code":
    #     st.echo()



@st.cache
def load_data(nrows):
    data = pd.read_csv("cannabis.csv", nrows=nrows, index_col=0)
    data = data.fillna("None")
    return data

data = load_data(10000)

def raw_data(data):
    st.markdown('## Raw Data: Cannabis Strains by Feature')
    st.dataframe(data, height=800, width=1500)

# Filtered Data Mode
def filter_data(data):
    
    # Effects
    from conjointanalysis_def import total_effects_list
    effect_selection = st.sidebar.selectbox('Strain Effect', total_effects_list)
    if effect_selection == "All Effects":
        effect_filter = pd.DataFrame(data)
    else:
        effect_filter = pd.DataFrame(data[data['Effects'].str.contains(effect_selection)])
    # st.write(effect_filter)

    # Flavor 
    from conjointanalysis_def import total_flavor_list
    # 'total_flavor', total_flavor

    flavor_selection = st.sidebar.selectbox('Strain Flavor',total_flavor_list)
    if flavor_selection == "All Flavors":
        flavor_filter = pd.DataFrame(data) 
    else:
        flavor_filter = pd.DataFrame(data[data['Flavor'].str.contains(flavor_selection)])
    # st.write(flavor_filter)

    # Rating
    rating_slider = st.sidebar.slider('Filter by Rating', 0,5)
    rating_filter = pd.DataFrame(data[data['Rating'] >= int(rating_slider)])


    # Result DataFrame

    st.write('## Top Strains by Filtered Selections')
    match_df = pd.DataFrame.merge(effect_filter, flavor_filter, on='Strain', how='inner')
    second_df = pd.DataFrame.merge(match_df, rating_filter, how='inner', on='Strain')
    final_df = pd.DataFrame.merge(second_df, type_filter, how='inner', on='Strain')
    # match_df = match_df[match_df['Flavor'].str.contains(flavor_selection)]
    # match_df = pd.DataFrame(flavor_filter,effect_filter)
    clean_df = final_df.drop(columns=['Type_y','Rating_y','Effects_y','Flavor_y','Description_y'])
    clean_df.columns = ['Type','Rating','Effects','Flavor','Description','a','b','c','d','e']
    page_df = clean_df.drop(columns=['a','b','c','d','e'])
    short_df = page_df.sort_values(by='Rating', ascending=False)
    st.dataframe(short_df,height=800, width=1500) 

# effects_options = filter_data(total_effects_list  )
# total_flavor_list = totalFlavor(data)

#''' MACHINE LEARNING MODE '''
# Load and cache functions and data.
def run_the_app():
    st.markdown("# Machine Learning")
    st.write("Answer the questions below to provide your input on what features you like and receive top recommendations:")

    # quiz_type = st.multiselect('Strain Type(s)', ('Any Type','sativa', 'indica', 'hybrid'))
    @st.cache
    def load_data(nrows):
        data = pd.read_csv("cannabis.csv", nrows=nrows, index_col=0)
        data = data.fillna("None")

    data = load_data(10000)
    from conjointanalysis_def import total_effects_list
    from conjointanalysis_def import total_flavor_list
    effect_input = st.multiselect('Most desired effects (choose 3)', total_effects_list)
    flavor_input = st.multiselect('Most craved flavors (choose 3)', total_flavor_list)

    

    if st.button("submit"):
        
    # @st.cache
    # def combo_df(effect_input, flavor_input):
        import random
        from conjointanalysis_def import total_rating
        sampled_list = random.sample(total_rating, 3)
        input_data = {'Type':['Indica', 'Sativa', 'Hybrid'], 'Strain Rating':sampled_list, 'Effect':effect_input, 'Taste':flavor_input} 

        # Start DataFrame 
        df = pd.DataFrame(input_data)

        # Adding Indica combos
        indica1 = pd.DataFrame({"Type":[df.Type[0]], "Strain Rating": [df["Strain Rating"][0]], "Effect": [df.Effect[1]], "Taste": [df.Taste[1]]})
        indica2 = pd.DataFrame({"Type":[df.Type[0]], "Strain Rating": [df["Strain Rating"][1]], "Effect": [df.Effect[1]], "Taste": [df.Taste[2]]})
        indica3 = pd.DataFrame({"Type":[df.Type[0]], "Strain Rating": [df["Strain Rating"][0]], "Effect": [df.Effect[2]], "Taste": [df.Taste[1]]})
        indica4 = pd.DataFrame({"Type":[df.Type[0]], "Strain Rating": [df["Strain Rating"][2]], "Effect": [df.Effect[2]], "Taste": [df.Taste[0]]})
        indica5 = pd.DataFrame({"Type":[df.Type[0]], "Strain Rating": [df["Strain Rating"][2]], "Effect": [df.Effect[0]], "Taste": [df.Taste[2]]})
        df = df.append(indica1, ignore_index = True)
        df = df.append(indica2, ignore_index = True)
        df = df.append(indica3, ignore_index = True)
        df = df.append(indica4, ignore_index = True)
        df = df.append(indica5, ignore_index = True)

        # Adding Sativa combos
        sativa1 = pd.DataFrame({"Type":[df.Type[1]], "Strain Rating": [df["Strain Rating"][2]], "Effect": [df.Effect[0]], "Taste": [df.Taste[0]]})
        sativa2 = pd.DataFrame({"Type":[df.Type[1]], "Strain Rating": [df["Strain Rating"][1]], "Effect": [df.Effect[0]], "Taste": [df.Taste[2]]})
        sativa3 = pd.DataFrame({"Type":[df.Type[1]], "Strain Rating": [df["Strain Rating"][0]], "Effect": [df.Effect[2]], "Taste": [df.Taste[0]]})
        sativa4 = pd.DataFrame({"Type":[df.Type[1]], "Strain Rating": [df["Strain Rating"][2]], "Effect": [df.Effect[2]], "Taste": [df.Taste[1]]})
        sativa5 = pd.DataFrame({"Type":[df.Type[1]], "Strain Rating": [df["Strain Rating"][2]], "Effect": [df.Effect[1]], "Taste": [df.Taste[2]]})
        df = df.append(sativa1, ignore_index = True)
        df = df.append(sativa2, ignore_index = True)
        df = df.append(sativa3, ignore_index = True)
        df = df.append(sativa4, ignore_index = True)
        df = df.append(sativa5, ignore_index = True)

        # Adding Hybrid combos
        hybrid1 = pd.DataFrame({"Type":[df.Type[2]], "Strain Rating": [df["Strain Rating"][1]], "Effect": [df.Effect[1]], "Taste": [df.Taste[0]]})
        hybrid2 = pd.DataFrame({"Type":[df.Type[2]], "Strain Rating": [df["Strain Rating"][2]], "Effect": [df.Effect[1]], "Taste": [df.Taste[1]]})
        hybrid3 = pd.DataFrame({"Type":[df.Type[2]], "Strain Rating": [df["Strain Rating"][0]], "Effect": [df.Effect[0]], "Taste": [df.Taste[0]]})
        hybrid4 = pd.DataFrame({"Type":[df.Type[2]], "Strain Rating": [df["Strain Rating"][0]], "Effect": [df.Effect[0]], "Taste": [df.Taste[2]]})
        hybrid3 = pd.DataFrame({"Type":[df.Type[2]], "Strain Rating": [df["Strain Rating"][0]], "Effect": [df.Effect[0]], "Taste": [df.Taste[0]]})
        hybrid5 = pd.DataFrame({"Type":[df.Type[2]], "Strain Rating": [df["Strain Rating"][0]], "Effect": [df.Effect[2]], "Taste": [df.Taste[1]]})
        df = df.append(hybrid1, ignore_index = True)
        df = df.append(hybrid2, ignore_index = True)
        df = df.append(hybrid3, ignore_index = True)
        df = df.append(hybrid4, ignore_index = True)
        df = df.append(hybrid5, ignore_index = True)

        # if st.checkbox("Show all results"):
        st.table(df)
        # combo_df.df = user_mix
        # return df
        st.markdown('## How likely are you to use a strain like this? (0 = Not Likely, 4 = Meh, 7 = Very Likely)')
        type_list = ['Indica', 'Sativa', 'Hybrid']
        from conjointanalysis_def import sampled_list

        first_input = {'Type':type_list[0], 'Strain Rating':sampled_list[0], 'Effect':effect_input[0], 'Taste':flavor_input[0]}
        second_input = {'Type':type_list[1], 'Strain Rating':sampled_list[1], 'Effect':effect_input[1], 'Taste':flavor_input[1]}
        third_input = {'Type':type_list[2], 'Strain Rating':sampled_list[2], 'Effect':effect_input[2], 'Taste':flavor_input[2]}
        df = df.append(second_input,ignore_index = True)
        df = df.append(third_input,ignore_index = True)

        st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row; align: center;}</style>', unsafe_allow_html=True)

        # if st.button("Yes!"):
            
        st.write(first_input)
        userinput1 = st.radio('1/18', (0,1,2,3,4,5,6,7))
        st.table(second_input)
        userinput2 = st.radio('2/18', (0,1,2,3,4,5,6,7))
        st.table(third_input)
        userinput3 = st.radio('3/18', (0,1,2,3,4,5,6,7))
        st.table(indica1)
        userinput4 = st.slider('4/18', 0,7)
        st.table(indica2)
        userinput5 = st.slider('5/18', 0,7)
        st.table(indica3)
        userinput6 = st.slider('6/18', 0,7)
        st.table(indica4)
        userinput7 = st.slider('7/18', 0,7)
        st.table(indica5)
        userinput8 = st.slider('8/18', 0,7)
        st.table(sativa1)
        userinput9 = st.slider('9/18', 0,7)
        st.table(sativa2)
        userinput10 = st.slider('10/18', 0,7)
        st.table(sativa3)
        userinput11 = st.slider('11/18', 0,7)
        st.table(sativa4)
        userinput12 = st.slider('12/18', 0,7)
        st.table(sativa5)
        userinput13 = st.slider('13/18', 0,7)
        st.table(hybrid1)
        userinput14 = st.slider('14/18', 0,7)
        st.table(hybrid2)
        userinput15 = st.slider('15/18', 0,7)
        st.table(hybrid3)
        userinput16 = st.slider('16/18', 0,7)
        st.table(hybrid4)
        userinput17 = st.slider('17/18', 0,7)
        st.table(hybrid5)
        userinput18 = st.slider('18/18', 0,7)

        MyRating = [userinput1, userinput2, userinput3, userinput4, userinput5, userinput6, userinput7, userinput8, userinput9, userinput10, userinput11, userinput12, userinput13, userinput14, userinput15, userinput16, userinput17, userinput18] 
        df['MyRating'] = MyRating
        df['MyRating'] = pd.to_numeric(df['MyRating'])
    # if st.button("Submit"):
    #     combo_df(effect_input, flavor_input)
    #     st.table(user_mix)

        # index_random = random.choice([0:18])

        # state = session_state.get(index_number=0)

        # @st.cache(suppress_st_warning=True)
        # def get_rate(index_number):
        #     # np.random.seed(question_number) - could consider adding this
        #     # arr = np.random.randint(1, 100, 2)
        #     arr = df.iloc[index_number]
        #     # q = f"{arr[0]} * {arr[1]}"
        #     q = st.write(arr)
        #     # i = 0
        #     # ans = arr[0]*arr[1]
        #     # choices = [0, ans, ans-1, ans+1, ans+2]
        #     choices = range(0,8)
        #     # return arr, q, ans, choices
        #     return arr, q, choices

        # # arr, q, ans, choices = get_rate(state.index_number)
        # arr, q, choices = get_rate(state.index_number)

        # # st.text(f"Option #{index_number}: {q}")
        # a = int(st.text_input('Rate:', choices))
        # user_rating = []
        # user_rating.append(a)
        
        
        # if st.button('Next'):
        #     state.index_number += 1
        #     raise RerunException(RerunData(widget_state=None))
            # if (a > 4):
            #     st.write("You like it!")
            # elif (a > 2):
            #     st.write(f"Just okay huh... lets try again")
            # else: 
            #     st.write(f"Hard nope!")


if __name__ == "__main__":
    main()