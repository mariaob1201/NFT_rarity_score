# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import pandas as pd

import functions
from functions import *
import plotly.express as px
import ast

qualities_df=pd.read_csv('output_score_yisus.csv')
qualities_df['Score_f']=100*qualities_df['Score']
N=len(qualities_df)

# GATHERING ON THE PLOT - SIMULATION
st.sidebar.markdown("## Plot Attributes")

# Selección del plot
reg = st.sidebar.selectbox(
    "Chose Region:",
    ['All'] + sorted(list(qualities_df['Region'].unique()))
)

ps = st.sidebar.selectbox(
    "Chose Plot Size:",
     [-1] + [8,16,32,64,128]
)

classif = st.sidebar.selectbox(
    "Chose Quality Class:",
    ['All'] + ['Meager','Fair','Rich','Lush','Bountiful']
)
min_score = st.sidebar.slider('Min Score', min_value=0, max_value=100, value=0 ,step=1)
max_score = st.sidebar.slider('Max Score', min_value=0, max_value=100, value=100 ,step=1)

st.sidebar.markdown("## Min number of deposits")
woods_size = st.sidebar.slider('Size of Wood Deposits', min_value=0, max_value=7, value=0,step=1)
stone_size = st.sidebar.slider('Size of Stone Deposits', min_value=0, max_value=7, value=0,step=1)
fabr_size = st.sidebar.slider('Size of Fabric Deposits', min_value=0, max_value=7, value=0,step=1)
met_size = st.sidebar.slider('Size of Metals Deposits', min_value=0, max_value=7, value=0,step=1)
gems_size = st.sidebar.slider('Size of Gem Deposits', min_value=0, max_value=7, value=0,step=1)
els_size = st.sidebar.slider('Size of Elements Deposits', min_value=0, max_value=7, value=0,step=1)


if 'All' in reg:
    if ps<1:
        qualities_df1 = qualities_df
    else:
        qualities_df1 = qualities_df[qualities_df['plot_size'] == ps]
    qualities_df3 = qualities_df1
else:
    qualities_df0 = qualities_df[qualities_df['Region']==reg]
    qualities_df3 = qualities_df0
    if ps<0:
        qualities_df1 = qualities_df0
    else:
        qualities_df1 = qualities_df0[qualities_df0['plot_size'] == ps]

if 'All' not in classif:
    qualities_df1 = qualities_df1[qualities_df1['Classification'] == classif]


qualities_df1 = qualities_df1[(qualities_df1['Woods_elements']>=woods_size) &
                            (qualities_df1['Stone_elements']>=stone_size) &
                            (qualities_df1['Fabrics_elements']>=fabr_size) &
                            (qualities_df1['Metals_elements']>=met_size) &
                            (qualities_df1['Gems_elements'] >= gems_size) &
                            (qualities_df1['Element_elements'] >= els_size)]

qualities_df1 = qualities_df1[qualities_df1['Score_f'] >= min_score]
qualities_df1 = qualities_df1[qualities_df1['Score_f'] <= max_score]



#print('**** ', qualities_df1.columns)

# GATHERING ON THE PLOT - SIMULATION
st.header("Plot Quality")
st.write(
    f""" Plot quality assigns an score from 1 to 100 to each plot. Here we present an statistical approach dependent on the collection:
    - An statistical methodology based on rarity weights
    https://bisonic.atlassian.net/wiki/spaces/META/pages/314081281/Rarity+Score+on+Plots
"""
)

st.write("THE CLASSIFICATION")
st.markdown("- Meager: 10 % of plots population with lowest score")
st.markdown("- Fair: plots population with score between [.11,.25]")
st.markdown("- Rich: plots population with score between [.26,.65] ")
st.markdown("- Lush: plots population with score between [.66,.90] ")
st.markdown("- Bountiful: plots population with score between [.91,1] ")


st.subheader('''Statistical Approach ''')
st.write(
    f""" 
            Methodology: https://bisonic.atlassian.net/wiki/spaces/META/pages/314081281/Rarity+Score+on+Plots
            The Final Score takes into account two preeliminar scores:

                - Scoring the deposit intensity: takes into account the plot size by a reserve multiplier and the essence strength in such existent deposit
                - Scoring the deposits existence by:
                    - Scoring the amount of deposits of certain family the plot has (a plot with 7 gems deposits is rarer in this attribute that other with 5)
                    - Scoring the total of deposits
    """
)


qua_p = qualities_df1.groupby(['Region'], as_index=False).agg({
    'plot_id': ['count'],
    'Score_f': ['mean','min','max','median', percentile(25), percentile(75), 'std']
})
qua_p['%']=qua_p[('plot_id', 'count')]/N
st.dataframe(qua_p)


fig_wd1 = px.scatter(qualities_df1, x="Number_of_elements", y=['Score_f'],
        size="plot_size",
        color="Classification",
        title=f"""Plot Score by Number of distinct elements available there""",
        hover_data=['Region','Score_Deposits','Class_Deposits', 'Class_Inensity','Score_Intensity',
            'Woods_elements', 'Stone_elements',
            'Fabrics_elements', 'Metals_elements', 'Gems_elements',
            'Element_elements' ], height=400)
fig_wd1.update_layout(
        xaxis_title="Number of distinct deposits available per plot", yaxis_title="Plot Score"
    )
st.plotly_chart(fig_wd1)

### How many plots
dict_elem = {}

dict_elem1 = {'Ash': 0,
 'Holly': 0,
 'Oak': 0,
 'Olive': 0,
 'Pine': 0,
 'Redwood': 0,
 'Willow': 0,
 'Alabaster': 0,
 'Basalt': 0,
 'Granite': 0,
 'Limestone': 0,
 'Marble': 0,
 'Sand': 0,
 'Shale': 0,
 'Cashmere': 0,
 'Cotton': 0,
 'Flax': 0,
 'Hemp': 0,
 'Jute': 0,
 'Silk': 0,
 'Wool': 0,
 'Aluminum': 0,
 'Copper': 0,
 'Iron': 0,
 'Tin': 0,
 'Titanium': 0,
 'Tungsten': 0,
 'Zinc': 0,
 'Amethyst': 0,
 'Diamond': 0,
 'Emerald': 0,
 'Ruby': 0,
 'Sapphire': 0,
 'Smoky Quartz': 0,
 'Topaz': 0,
 'Antimony': 0,
 'Calcium': 0,
 'Carbon': 0,
 'Hydrogen': 0,
 'Nitrogen': 0,
 'Silicon': 0,
 'Sulfur': 0}

for key, value in qualities_df1.iterrows():

    # Convert the elements to integers
    res = ast.literal_eval(qualities_df1.at[key, "List_of_elements"])  # .strip('][').split(', ')
    res1 = [i.replace('_tint', '') for i in res]
    res2 = list(set(res1))

    for el1 in res2:
        dict_elem1[el1] += 1

x=list(dict_elem1.keys())
y=list(dict_elem1.values())

dict_f = {}
dict_f['Deposits'] = dict_elem1.keys()
dict_f['Vol'] = dict_elem1.values()

dframe = pd.DataFrame.from_dict(dict_f)
dframe2=dframe[dframe['Vol']>0]


fig11 = px.pie(dframe2, values='Vol', names='Deposits')
fig11.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))


st.plotly_chart(fig11)
st.dataframe(dframe2)


