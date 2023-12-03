import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
from streamlit_option_menu import option_menu


mydb = psycopg2.connect(
    host = "localhost",
    database = "postgres",
    user = "postgres",
    password = "123456")

mycursor = mydb.cursor()


df = pd.read_csv(r"D:\phonepe_project\pulse\year.csv")
st.set_page_config(page_title = "Phone_pe Pulse",
                #    page_icon = icon,
                   layout = 'wide',
                   initial_sidebar_state = 'expanded',
                   menu_items = {'About': """# This app is used to analyze Phonepe Pulse data
                                                Created BY *Prakash*"""})
st.title("Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly")

with st.sidebar:
    selected = option_menu(None, ["Home" , "Aggregated Data", "Map Data", "Top Transaction & User Data" ],
                            icons = ["house-door-fill","tools"],
                            default_index = 0 ,
                            orientation = "v",
                            styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#33A5FF"},
                                   "icon": {"font-size": "30px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#33A5FF"}})
    
    
    if selected == "Aggregated Data":
        quater_selected = st.radio("Select a Quater", [1, 2, 3, 4], key='home_quater')
        year_selected = st.selectbox("Select a Year", df['year'], key='home_year')

    if selected == "Map Data":
        quater_selected = st.radio("Select a Quater", [1, 2, 3, 4], key='home_quater')
        year_selected = st.selectbox("Select a Year", df['year'], key='home_year')
    
    if selected == "Top Transaction & User Data":
        quater_selected = st.radio("Select a Quater", [1, 2, 3, 4], key='home_quater')
        year_selected = st.selectbox("Select a Year", df['year'], key='home_year')
        
# Create Homee page    
if selected == "Home":
    col1,col2 =st.columns(2, gap = 'medium')

    col1.markdown("### :blue[Title] : Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly")
    col1.markdown("### :blue[Overview] : This Streamlit app is used analyze the data provided by phonepe pulse and ploting a geo map.")
    col1.markdown("### :blue[Technologies Used] : Python, Streamlit, Pandas, Plotly Express, PostgreSql, Psycopg2 and SQL Alchemy")

# Analyze the data
if selected == "Aggregated Data":

    tab1, tab2 = st.tabs(["$\huge Transactions $", "$\huge Users $"])

    with tab1:
        st.write("##  Aggregated Transaction Data Analysis:")
        col1, col2 = st.columns(2, gap='medium')

        sql_query = f"""select state, transaction_type, sum(transaction_count) as transaction_count, 
                        sum(transaction_amount) as transaction_amount from agg_trans
                        where quater = '{quater_selected}' and year ='{year_selected}'
                        group by state, 
                        transaction_type
                        order by transaction_amount desc
                    """
        mycursor.execute(sql_query)

        # Create a DataFrame from the SQL query result
        df1 = pd.DataFrame(mycursor.fetchall(), columns = [desc[0] for desc in mycursor.description])
        fig = px.histogram(df1, x = 'transaction_amount', 
                    y = 'state', 
                    labels = {'state': 'State', 'transaction_amount': 'Transaction Amount'})
        
        fig.update_layout(width = 500)

        col1.plotly_chart(fig)


        # Convert 'transaction_count' to numeric type
        df1['transaction_count'] = pd.to_numeric(df1['transaction_count'], errors = 'coerce')

        # Select top 10 states based on total transaction count
        top_states = df1.groupby('state')['transaction_count'].sum().nlargest(10).index

        df_top_states = df1[df1['state'].isin(top_states)]

        # Create polar bar chart for top 10 states and all transaction types
        fig2 = px.bar_polar(df_top_states, r = 'transaction_count', theta = 'state', color = 'transaction_type',
               labels = {'transaction_amount': 'Transaction Amount'},
               title = 'Polar Bar Chart: Top 10 States with Highest Transactions')


        fig2.update_layout(width=500)

        col1.plotly_chart(fig2)

        # Display the data in the second column
        col2.write("Transaction Data:")
        col2.write(df1)

        fig3 = px.pie(df1, values = 'transaction_count',
                    names = 'transaction_type',
                    title = 'Transaction Count',
                    hover_data = 'transaction_type')
        
        fig3.update_layout(width = 500)

        col2.plotly_chart(fig3)
    
    with tab2:
        st.write("##  Aggregated User Data Analysis:")
        col1, col2 = st.columns(2, gap = 'medium')


        sql_query2 = f"""select state,  brand_name, sum(brand_count) as brand_count, 
                        sum(brand_usage)  as brand_usage from agg_user
                        where quarter = '{quater_selected}' and year ='{year_selected}'
                        group by state, brand_name
                    """
        mycursor.execute(sql_query2)

        # Create a DataFrame from the SQL query result
        df1 = pd.DataFrame(mycursor.fetchall(), columns=[desc[0] for desc in mycursor.description])
        fig = px.histogram(df1, x = 'state', 
                    y = 'brand_count', 
                    color = 'brand_name',
                    labels = {'brand_name': 'Brand Name', 'brand_count': 'Brand Count'})
        
        fig.update_layout(width=500)

        col1.plotly_chart(fig)

        # Display the data in the second column
        col2.write("User Data:")
        col2.write(df1)

        fig2 = px.pie(df1, values = 'brand_count',
                    names = 'brand_name',
                    title = 'Brand Count',
                    hover_data = 'brand_name')
        
        fig2.update_layout(width = 500)

        col2.plotly_chart(fig2)

        df1['brand_count'] = pd.to_numeric(df1['brand_count'], errors = 'coerce')

        # Select top 10 states based on total brand count
        top_states = df1.groupby('state')['brand_count'].sum().nlargest(10).index

        # Filter the DataFrame for the top 10 states
        df_top_states = df1[df1['state'].isin(top_states)]

        # Create polar bar chart for top 10 states and all brand types
        fig3 = px.bar_polar(df_top_states, r = 'brand_count', theta = 'state', color = 'brand_name',
                    labels = {'brand_count': 'Brand Count'},
                    title = 'Polar Bar Chart: Top 10 States with Highest Brand usage')

        fig3.update_layout(width = 500)

        col1.plotly_chart(fig3)


if selected == "Map Data":

    tab1, tab2 = st.tabs(["$\huge Transactions $", "$\huge Users $"])

    with tab1:

        st.write("### Map data Analysis for Transactions")

        query3 = f"""SELECT state, sum(transaction_count) as transaction_count, 
                    sum(transaction_amount) as transaction_amount FROM map_trans
                    where quater = '{quater_selected}' and year ='{year_selected}'
                    group by state 
                    order by transaction_amount desc
                    """

        # Execute the query
        mycursor.execute(query3)

        

        df3 = pd.DataFrame(mycursor.fetchall(), columns = [desc[0] for desc in mycursor.description])
        df3['state'] = df3['state'].str.replace('-', ' ').str.title()
        df3['state'] = df3['state'].str.replace(' Islands', '')
        st.write(df3)

        fig = px.choropleth(
            df3,
            geojson = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey = 'properties.ST_NM',  # Update this based on your GeoJSON file structure
            locations = 'state',
            color = 'transaction_amount',
            color_continuous_scale = 'Reds',  # You can adjust this color scale
            hover_data = ["state", "transaction_amount"]
        )

        fig.update_geos(fitbounds = "locations", visible = False)

        fig.update_layout(
            geo=dict(bgcolor = '#270C34'),
            paper_bgcolor = '#270C34',
            coloraxis_colorbar = dict(
                title = {'text': 'Transaction Amount', 'font': {'color': 'white', 'size': 20}},
                tickfont = dict(color = 'white', size = 20)
            ),
            hoverlabel = dict(
                bgcolor = '#FFDC2C',  # background color
                font=dict(color = 'black', size = 20),  # font color and size
                bordercolor = 'rgba(255, 0, 0, 0.2)',  # border color
            ),
            height = 800,
            width = 700
        )

        st.plotly_chart(fig, use_container_width = True)

    with tab2:
        st.write("### Map data Analysis for Users")

        query4 = f"""SELECT state, sum(registered_users) as users, 
                    sum(app_opens) as app_opens FROM map_user
                    where quater = '{quater_selected}' and year ='{year_selected}'
                    group by state 
                    order by app_opens desc
                    """

        # Execute the query
        mycursor.execute(query4)

        

        df4 = pd.DataFrame(mycursor.fetchall(), columns = [desc[0] for desc in mycursor.description])
        st.write(df4)

        fig = px.histogram(df4, x = 'state', y = ['app_opens', 'users'], color_discrete_map={'users': 'yellow', 'app_opens': 'cyan'},
                 labels = {'state': 'State', 'value': 'Count'}, barmode = 'stack',
                 title = 'Stacked Bar Chart: Users and App Opens')

        st.plotly_chart(fig, use_container_width = True)


if selected == "Top Transaction & User Data":
    tab1, tab2 = st.tabs(["$\huge Transactions $", "$\huge Users $"])

    with tab1:
        col1, col2 = st.columns(2, gap = 'medium')

        df_state = pd.read_csv(r'D:\phonepe_project\pulse\state.csv')
        
        
        state_selected = col1.selectbox("Select a State", df_state['state'], key = 'home_state')
        query5 = f"""
                    select state, pincode, transaction_amount
                    from top_trans
                    where quater = '{quater_selected}' and year ='{year_selected}' and state = '{state_selected}'
                    """
        mycursor.execute(query5)

        df5 = pd.DataFrame(mycursor.fetchall(), columns = [desc[0] for desc in mycursor.description])
        df5["pincode"] = df5["pincode"].astype(str).apply(lambda x: x.rstrip('0').rstrip('.') if '.' in x else x)

        
        col1.markdown("### Top Transaction Data on each Pincodes:")
        col1.write(df5)

        fig = px.pie(df5, values = 'transaction_amount',
                           names = 'pincode',
                           labels = {'transactin_amount' : 'Transaction Amount' , 'pincode': 'Pincodes'},
                           hover_data = 'pincode'
                            )


        col2.markdown(f" ### Top 10 pincodes with Highest transaction in '{state_selected}'")

        fig.update_traces(textposition = 'inside', textinfo = 'percent+label',textfont = dict(size = 30))
        col2.plotly_chart(fig, use_container_width = 500)


    with tab2:
         
        col1, col2 = st.columns(2, gap = 'medium')

        df_state = pd.read_csv(r'D:\phonepe_project\pulse\state.csv')
        
        
        state_selected = col1.selectbox("Select a State", df_state['state'], key = 'home_state2')
        query6 = f"""
                    select state, pincode, registered_users
                    from top_user
                    where quater = '{quater_selected}' and year ='{year_selected}' and state = '{state_selected}'
                    """
        mycursor.execute(query6)

        df6 = pd.DataFrame(mycursor.fetchall(), columns = [desc[0] for desc in mycursor.description])
        
        col1.markdown("### Top User Data on each Pincodes:")
        col1.write(df6)


        fig = px.pie(df6, values = 'registered_users',
                           names = 'pincode',
                           labels = {'registered_users' : 'Registered Users' , 'pincode': 'Pincodes'},
                           hover_data = 'pincode'
                            )


        col2.markdown(f"### Top 10 pincodes with Highest transaction in '{state_selected}'")

        fig.update_traces(textposition = 'inside', textinfo =' percent+label',textfont = dict(size = 30))
        col2.plotly_chart(fig, use_container_width = 500)