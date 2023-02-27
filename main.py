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
st.sidebar.markdown("## General Controls")

# Selección del plot
reg = st.sidebar.selectbox(
    "Chose Region for Qualities:",
    ['All'] + sorted(list(qualities_df['Region'].unique()))
)

ps = st.sidebar.selectbox(
    "Chose Plot Size for Qualities:",
     [-1] + [8,16,32,64,128]
)

classif = st.sidebar.selectbox(
    "Chose Quality Class:",
    ['All'] + ['Meager','Fair','Rich','Lush','Bountiful']
)

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

#print('**** ', qualities_df1.columns)

# GATHERING ON THE PLOT - SIMULATION
st.header("Plot Quality")
st.write(
    f""" Plot quality assigns an score from 1 to 100 to each plot. Here we present two approaches, 
    both of them are dependent on the collection:
    - An statistical methodology based on rarity weights
    https://bisonic.atlassian.net/wiki/spaces/META/pages/314081281/Rarity+Score+on+Plots
    - An frequentist methodology based on distribution. 
"""
)

st.write("THE CLASSIFICATION")
st.markdown("- Meager: 10 % of plots population with lowest score")
st.markdown("- Fair: plots population with score between [.11,.25]")
st.markdown("- Rich: plots population with score between [.26,.65] ")
st.markdown("- Lush: plots population with score between [.66,.94] ")
st.markdown("- Bountiful: plots population with score between [.95,1] ")


st.subheader('''Statistical methodology ''')
st.write(
    f""" 
            Methodology: https://bisonic.atlassian.net/wiki/spaces/META/pages/314081281/Rarity+Score+on+Plots
            The Final Score takes into account two preeliminar scores:

                - Scoring the material intensity: takes into account the plot size that have a bigger scale in material storage, and at the same time takes into account the essence strength per each material available in such existent deposits
                - Scoring the deposits existence measures two things:
                    - Scoring the amount of materials for all the deposits the plot has
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
        xaxis_title="Number of distinct materials available in single plot", yaxis_title="Plot Score"
    )
st.plotly_chart(fig_wd1)


### How many plots
dict_elem = {}
"""split = qualities_df1["List_of_elements"].apply(pd.Series)
split = split.rename(columns = lambda x : 'val_' + str(x))
st.dataframe(split)

split.melt(value_name="val").groupby(["val"]).size()
st.dataframe(split)"""

dict_elem1 = functions.dict_elem

for key, value in qualities_df1.iterrows():
    # print('Here ', key, qualities_df1.at[key, "List_of_elements"])
    # Extract the elements of the list from the string
    # elements = re.findall(r'\d+', qualities_df1.at[key, "List_of_elements"])

    # Convert the elements to integers
    res = ast.literal_eval(qualities_df1.at[key, "List_of_elements"])  # .strip('][').split(', ')
    res1 = [i.replace('_tint', '') for i in res]
    res2 = list(set(res1))
    # [int(x) for x in elements]
    # print(type(res),res)
    for el1 in res2:
        dict_elem1[el1] += 1

#elements=pd.DataFrame.from_dict(dict_elem1)
#st.dataframe(elements)

st.write(
    f""" Elements {dict_elem1} """
)

"""
st.dataframe(elements)
fig_elements = px.bar(elements, x="plot_size", y=['Gems__Deposits', 'Element__Deposits',
       'Metals__Deposits', 'Fabrics__Deposits',
       'Woods__Deposits', 'Stone__Deposits'],log_y=True,
                title="Total deposits per plot size taking all the plots into account", barmode='group',
             height=400)
fig_elements.update_xaxes(categoryorder='array', categoryarray= ['8x8','16x16','32x32','64x64','128x128'])
st.plotly_chart(fig_elements)"""

