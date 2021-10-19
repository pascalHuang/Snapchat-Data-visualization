import streamlit as st
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import json 
import seaborn as sns

st.set_page_config(layout="wide")
sns.color_palette()

st.title('Huang Pascal Snapchat Data visualization')

st.title('Text messages')

json_data = open('chat_history.json').read()
data = json.loads(json_data)

st.header('Splitting the Data into 2 lists of dict ')

received_chat = data['Received Chat History']
send_chat = data['Sent Chat History']

st.write("1 item in the list received")
st.write(received_chat[1])
st.write("1 item in the list send")
st.write(send_chat[1])

st.header('Creating DataFrames')

df_received = pd.DataFrame(received_chat)
df_send = pd.DataFrame(send_chat)

st.write('df received')
st.write(df_received.head())
st.write('df send')
st.write(df_send.head())

st.header('Transforming the Data')
df_received['Created'] = df_received['Created'].map(pd.to_datetime)
df_send['Created'] = df_send['Created'].map(pd.to_datetime)

def get_y(dt): 
    return dt.year

df_received['year'] = df_received['Created'].map(get_y)
df_send['year'] = df_send['Created'].map(get_y)

def get_moy(dt): 
    return dt.month 

df_received['month'] = df_received['Created'].map(get_moy)
df_send['month'] = df_send['Created'].map(get_moy)

def get_dow(dt): 
    return dt.weekday() + 1

df_received['day_of_week'] = df_received['Created'].map(get_dow)
df_send['day_of_week'] = df_send['Created'].map(get_dow)

def get_dom(dt): 
    return dt.day 

df_received['day_of_month'] = df_received['Created'].map(get_dom)
df_send['day_of_month'] = df_send['Created'].map(get_dom)

def get_hour(dt): 
    return dt.hour

df_received['hour'] = df_received['Created'].map(get_hour)
df_send['hour'] = df_send['Created'].map(get_hour)

st.write('Extraction the day of month, the day of week, the year, the month, the hour')
st.write(df_received.head())
st.write(df_send.head())

st.title('Visualizing the type of media exchanged')

map1 = st.columns(2)
map1[1].write('30 000 messages received')
fig = plt.figure()
sns.countplot(y="Media Type", data = df_received[["Media Type"]], color="#BE313B")


map1[0].write('50 000 messages sent')
fig4 = plt.figure()
sns.countplot(y="Media Type", data = df_send[["Media Type"]], color="#316EBE")

map1[0].pyplot(fig4)
map1[1].pyplot(fig)



map = st.columns(1)
map[0].title('plotting all my friend messages')
fig2 = plt.figure(figsize = (100, 60))
sns.countplot(y="From", data = df_received[["From"]], color="#BE313B", order=df_received['From'].value_counts().index)
sns.countplot(y="To", data = df_send[["To"]], color="#316EBE", order=df_send['To'].value_counts().index)
map[0].pyplot(fig2)
map[0].write('As we can see I talk to a small part of my friend so I decided to make a top 10 of my friend who I talk the most.')



total_messages_received = df_received.groupby('From').count()
total_messages_received = total_messages_received.sort_values(by=["Created"])

def top_10(total_messages):
    for k in range(len(total_messages)):
        if len(total_messages) > 10:
            total_messages.drop(total_messages.index[:1], inplace=True)
        else:
            return
    return

top10received = total_messages_received
top_10(top10received)
top10received = top10received.sort_values(by=["Created"], ascending=False)


map[0].title('Top 10 friends')


map2 = st.columns(2)
map2[0].header('Top 10 friends who sent me the most messages')
fig3 = plt.figure()
top10received['Created'].plot.bar(color='#BE313B')
map2[0].pyplot(fig3)

total_messages_send = df_send.groupby('To').count()
total_messages_send = total_messages_send.sort_values(by=["Created"])
top10send = total_messages_send
top_10(top10send)
top10send = top10send.sort_values(by=["Created"], ascending=False)

map2[1].header('Top 10 friends I sent the most messages')
fig5 = plt.figure()
top10send['Created'].plot.bar(color='#316EBE')
map2[1].pyplot(fig3).pyplot(fig5)

map2[0].title('Messages activity by year')
map2[0].write('red = received')
map2[0].write('blue = sent')
fig6 = plt.figure()
sns.countplot(y="year", data = df_received[["year"]], color="#BE313B")
sns.countplot(y="year", data = df_send[["year"]], color="#316EBE")
map2[0].pyplot(fig6)


map3 = st.columns(2)
map3[0].title('Messages activity by month')
map3[0].write('red = received')
map3[0].write('blue = sent')
fig7 = plt.figure()
sns.countplot(y="month", data = df_received[["month"]], color="#BE313B")
sns.countplot(y="month", data = df_send[["month"]], color="#316EBE")
plt.yticks(np.arange(12), 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())
map3[0].pyplot(fig7)

map4 = st.columns(2)
map4[0].title('Messages activity by day of week')
map4[0].write('red = received')
map4[0].write('blue = sent')
fig8 = plt.figure()
sns.countplot(y="day_of_week", data = df_received[["day_of_week"]], color="#BE313B")
sns.countplot(y="day_of_week", data = df_send[["day_of_week"]], color="#316EBE")
plt.yticks(np.arange(7), 'Mon Tue Wed Thu Fri Sat Sun'.split())
map4[0].pyplot(fig8)

map5 = st.columns(2)
map5[0].title('Messages activity by day of month')
map5[0].write('red = received')
map5[0].write('blue = sent')
fig9 = plt.figure()
sns.countplot(y="day_of_month", data = df_received[["day_of_month"]], color="#BE313B")
sns.countplot(y="day_of_month", data = df_send[["day_of_month"]], color="#316EBE")
map5[0].pyplot(fig9)

map6 = st.columns(2)
map6[0].title('Messages activity by hour (UTC)')
map6[0].write('red = received')
map6[0].write('blue = sent')
fig10 = plt.figure()
sns.countplot(y="hour", data = df_received[["hour"]], color="#BE313B")
sns.countplot(y="hour", data = df_send[["hour"]], color="#316EBE")
map6[0].pyplot(fig10)

map6[0].title('Snapchat location (last 6 months)')
json_data = open('location_history.json').read()
location = json.loads(json_data)

location_history = location['Location History']
dflocation = pd.DataFrame(location_history)

dflocation["Latitude, Longitude"][1]
dflocation[['Latitude1','Longitude1']] = dflocation['Latitude, Longitude'].str.split(",",expand=True)
dflocation[['latitude','erreur1']] = dflocation['Latitude1'].str.split("±",expand=True)
dflocation[['longitude','erreur2']] = dflocation['Longitude1'].str.split("±",expand=True)
dflocation["latitude"] = pd.to_numeric(dflocation["latitude"], downcast="float")
dflocation["longitude"] = pd.to_numeric(dflocation["longitude"], downcast="float")

st.map(dflocation[['longitude', 'latitude']], zoom=11)

import pydeck as pdk
st.pydeck_chart(pdk.Deck(
   map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=48.8588336,
         longitude=2.2769952,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=dflocation,
            get_position='[longitude, latitude]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=location,
             get_position='[longitude, latitude]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
))