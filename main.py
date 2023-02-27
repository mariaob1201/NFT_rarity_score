# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import pandas as pd

from depositchances import *
import plotly.express as px

qualities_df=pd.read_csv('output_score_yisus.csv')
def fun(x):
    if len(x)<4:
        return 8
    else:
        return int(x[:2])

# GATHERING ON THE PLOT - SIMULATION
st.sidebar.markdown("## 4. Controls for Plot Quality")
# Selección del plot
reg = st.sidebar.selectbox(
    "Chose Region for Qualities:",
    ['All'] + list(data0['Region'].unique())
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
    qualities_df3 = qualities_df
    if ps<1:
        qualities_df1 = qualities_df
    else:
        qualities_df1 = qualities_df[qualities_df['plot_size'] == ps]
else:
    qualities_df0 = qualities_df[qualities_df['Region']==reg]
    qualities_df3 = qualities_df0
    if ps<0:
        qualities_df1 = qualities_df0
    else:
        qualities_df1 = qualities_df0[qualities_df0['plot_size'] == ps]

if 'All' not in classif:
    qualities_df1 = qualities_df1[qualities_df1['Classification'] == classif]

fig_wd1 = px.scatter(qualities_df1, x="Number_of_elements", y=['Score'],
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
    'Score': ['min','max','median','mean','std']
})
qua_p['%']=qua_p[('plot_id', 'count')]/9650
st.dataframe(qua_p)
