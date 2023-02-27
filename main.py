# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import pandas as pd
from functions import *
import plotly.express as px

qualities_df=pd.read_csv('output_score_yisus.csv')
qualities_df['Score_f']=100*qualities_df['Score']

# GATHERING ON THE PLOT - SIMULATION
st.sidebar.markdown("## General Controls")

# Selección del plot
reg = st.sidebar.selectbox(
    "Chose Region for Qualities:",
    ['All'] + list(qualities_df['Region'].unique())
)

ps = st.sidebar.selectbox(
    "Chose Plot Size for Qualities:",
     [-1] + [8,16,32,64,128]
)

classif = st.sidebar.selectbox(
    "Chose Quality Class:",
    ['All'] + ['Rich','Lush','Meager','Fair','Bountiful']
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



# GATHERING ON THE PLOT - SIMULATION
st.header("Plot Quality")
st.write(
    f""" Plot quality assigns an score from 1 to 100 to each plot. Here we present two approaches, 
    both of them are dependent on the collection:
    - An statistical methodology based on rarity weights
    https://bisonic.atlassian.net/wiki/spaces/META/pages/314081281/Rarity+Score+on+Plots
    - An frequentist methodology based on distribution. 

    THE CLASSIFICATION:
            - Meager: 10 % of plots population with lowest score
            - Fair: plots population with score between [.11,.25]
            - Rich: plots population with score between [.26,.65] 
            - Lush: plots population with score between [.66,.94]       
            - Bountiful: plots population with score between [.95,1] 
"""
)


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


qua_p = qualities_df3.groupby(['Region'], as_index=False).agg({
    'plot_id': ['count'],
    'Score_f': ['min','max','median','std', percentile(25), 'mean', percentile(75)]
})
qua_p['%']=qua_p[('plot_id', 'count')]/9650
st.dataframe(qua_p)
