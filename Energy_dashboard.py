import streamlit as st 
import pandas as pd 
import datetime
import plotly_express as px 
from warnings import filterwarnings
filterwarnings(action='ignore')

st.set_page_config(
    page_title='Energy Consumption',
    page_icon=":bar_chart:",
    layout='wide'
)

st_hide_style = ('''
    <style>        
     #MainMenu{visibility:hidden}
     Header{visibility:hidden}
     Footer{visibility:hidden}
     div.block-container{padding: 0.5rem 1rem}         
    </style>''')

st.markdown(st_hide_style, unsafe_allow_html=True)

st.title('Energy Consumption Dashbaord :bar_chart:')

df = pd.read_csv('Energy_consumption.csv')

df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
df['Date'] = df['Date'].map(datetime.datetime.date)

df['Time'] = pd.to_datetime(df['Timestamp']).dt.time
df['Time'] = pd.to_datetime(df['Time'], format="%H:%M:%S")
df['Time'] = df['Time'].map(datetime.datetime.time)

start_date = pd.to_datetime(df['Date']).min()
end_date = pd.to_datetime(df['Date']).max()

start_time = df['Time'].min()

end_time = df['Time'].max()

firstdate,starttime,lastdate,endtime = st.columns([2,1,2,1])
with firstdate:
    first_date = st.date_input('Start date', start_date)
with lastdate:
    last_date = st.date_input('End Date', end_date)
df1 = df[(df['Date'] >= first_date) & (df['Date'] <= last_date)]

with starttime:
    firsttime = st.time_input("Enter initial time", start_time)
   
with endtime:
    lasttime = st.time_input("Enter last time", end_time)
    
df2 = df1[(df1['Time'] >= firsttime) & (df1['Time'] <= lasttime)]

df2['DayOfWeek'] = pd.to_datetime(df2['Timestamp']).dt.day_name()

df2['Weeknumber'] = pd.to_datetime(df2['Timestamp']).dt.weekday

st.dataframe(df2, use_container_width=True, height=300)

temp_and_energy_consumption = df2.groupby(by=['Temperature'], as_index=False)['EnergyConsumption'].sum()

fig = px.line(data_frame=temp_and_energy_consumption, x= temp_and_energy_consumption['Temperature'], y= temp_and_energy_consumption['EnergyConsumption'], title='Energy consumption vs Temperature')
st.plotly_chart(fig, use_container_width=True)

DayofWeek_and_consumption = df2.groupby(by=['DayOfWeek','Weeknumber'], as_index=False)['EnergyConsumption'].sum().sort_values('Weeknumber', ascending=True)

fig2 = px.bar(DayofWeek_and_consumption, x= 'DayOfWeek', y='EnergyConsumption', title= 'Energy Consumption with respect to Week', text= ['{:,.2f}'.format(x) for x in DayofWeek_and_consumption['EnergyConsumption']])

st.plotly_chart(fig2, use_container_width=True)

Holiday_and_Energyconsumption = df2.groupby(['Holiday'], as_index=False)['EnergyConsumption'].sum()

fig3 = px.pie(data_frame=Holiday_and_Energyconsumption, names= Holiday_and_Energyconsumption['Holiday'], values=Holiday_and_Energyconsumption['EnergyConsumption'], title= 'Holiday and Energy Consumption', hole=0.5)

st.plotly_chart(fig3, use_container_width=True)