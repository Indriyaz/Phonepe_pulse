import pandas as pd
import plotly.express as px
import streamlit as st
import mysql.connector

options_y = ["2018", "2019", "2020"]
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

st.sidebar.markdown('''
---
Created with ❤️ by [Indriyaz](https://www.linkedin.com/in/riyaz-sk).
''')

# Connect to the MySQL database
cnx = mysql.connector.connect(
  host="sql680.main-hosting.eu",
  user="u673779311_python",
  password="P16@pythonp",
  database="u673779311_sql"
)




# Execute the SELECT statement to retrieve the data
table_name = f"{selected_option}_{selected_option_y}_{selected_option_q}"
query = f"SELECT * FROM {table_name}"
query_1 = f"SELECT * FROM TRANS_{selected_option_y}_{selected_option_q}"
df = pd.read_sql_query(query, cnx)


# Row A
st.markdown('### Transactions')
df2 = pd.read_sql_query(query_1, cnx)
df2["count"] = df2["count"]
total=df2["count"].sum()
total_f='{:0,.3f} Cr'.format(total/100000000)
df2["amount"] = df2["amount"]
total_v=df2["amount"].sum()
total_v_f="₹{:,.0f} Cr".format(total_v/100000000)
avg_v=total_v/total
avg_v_f = "₹{:,.0f}".format(avg_v)

col1, col2, col3 = st.columns(3)
col1.metric("All PhonePe transactions (UPI + Cards + Wallets)",total_f)
col2.metric("Total payment value",total_v_f)
col3.metric("Avg.transaction value",avg_v_f)


c1, c2 = st.columns((5,5))
with c1:
    st.markdown('### GEOMAP')
    fig = px.choropleth(
            df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='name',
            color='count',
            color_continuous_scale='blues',
            hover_name="name",
            hover_data=["count", "amount"]
        )

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)

with c2:
    st.markdown('### Donut chart')


    fig1 = px.pie(df2, values='count', names='name', title='Transactions',hole=.2,
                      hover_data=['count'], labels={'count':'Transactions'})
    fig1.update_traces(textposition='auto', textinfo='percent+label')
    st.plotly_chart(fig1)

c5 ,c6 =st.columns((5,5))
with c5:
   st.header("State Wise Table")
   st.dataframe(df[["count", "amount", "name"]],800)
with c6:
   st.header("Category Wise Table")
   st.dataframe(df2[["count", "amount", "name"]], 800)

cnx.close()
print (df)