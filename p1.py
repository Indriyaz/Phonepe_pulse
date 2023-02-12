import pandas as pd
import plotly.express as px
import streamlit as st
import mysql.connector

options_y = ["2018", "2019"]
options = ["MAP"]
options_q = ["Q1", 'Q2',"Q3", "Q4"]

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

with st.sidebar:
    selected_option_y = st.selectbox("Select a Year", options_y)
with st.sidebar:
    selected_option = st.selectbox("Select Map", options)
with st.sidebar:
    selected_option_q = st.selectbox("Select a Quarter", options_q)

# Connect to the MySQL database
cnx = mysql.connector.connect(
  host="sql680.main-hosting.eu",
  user="u673779311_python",
  password="P16@pythonp",
  database="u673779311_sql"
)




# Execute the SELECT statement to retrieve the data
table_name = f"{selected_option_y}_{selected_option}_{selected_option_q}"
query = f"SELECT * FROM {table_name}"
query_1 = "SELECT * FROM 2018_trans"
df = pd.read_sql_query(query, cnx)


# Row A
st.markdown('### Metrics')
df2 = pd.read_sql_query(query_1, cnx)
total=df2["count"].sum()
df3= df2[["name","count"]]

col1, col2, col3 = st.columns(3)
col1.metric(" Transctions",total)
col2.metric("Hello",total)
col3.metric("Humidity", "86%", "4%")


c1, c2 = st.columns((5,5))
with c1:
    st.markdown('### GEOMAP')

    if selected_option_y == "2018" and selected_option == "MAP" and selected_option_q == "Q1":

        fig = px.choropleth(
            df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='name',
            color='count',
            range_color=(0,10),
            color_continuous_scale='Reds',
            hover_name="name",
            hover_data=["count", "amount"]
        )

        fig.update_geos(fitbounds="locations", visible=False)


        st.plotly_chart(fig)

with c2:
    st.markdown('### Donut chart')
    if selected_option_y == "2018":
       
        fig1 = px.pie(df2, values='count', names='name', title='Transactions',hole = .3
                      hover_data=['count'], labels={'count':'Transactions'})
        fig1.update_traces(textposition='auto', textinfo='percent+label')
        st.plotly_chart(fig1)
c5 ,c6 =st.columns((5,5))
with c5:
   st.dataframe(df[["count", "amount", "name"]],800)

cnx.close()
