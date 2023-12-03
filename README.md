# Phonepe_pulse_analysis
# Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly

Hi everyone,
I have created a streamlit app to analuze the data from the Phonepe Pulse github repository(https://github.com/PhonePe/pulse) from 2018 1st quater to 2023 3rd quater.

In this app we can get the insights of the Transactions, Existing App users, New users, Which device they use, Which mode of payments they do, Which states are higheer in transactions, and in which area phonepe could concentrate more to develope ther business.


## Technologies Used.

I used python to code,
### Libraries Used:
1 Streamlit

2 Plotly Express

3 Pandas

4 Psycopg2

5 SQL Alchemy


## Steps Involved:

1. First I used to extract the data from phonepe pulse repository using github cloning, Then The Studied each files which is given in a json format, Then I converted the data into a csv.

2. Then created Tables on PostgreSQL to add and query the data from The csv files. Though we can directly frame and plot the datat using csv files, but for the effective analysis I used SQL query for dataframe and ploting

3. The added the table data using sqlalchemy engine, to prevent duplicate data appending in table.

4. Then querried out the reqired data from Aggregated transactions and users data to get the top transactions and top used devices plots, I used histogram and pie charts for this analysis.

5. Then plotted a map using geojson data, With this I plotted India map with all the states transaction data.

6. Then Used the Top transaction and users data to plot how many users are there and how many new users joined in the nex quater, and The total transaction amount in each pincodes.

7. I also added a Radio Button and Selectbox for quater and year respectivly dor distinctive analysis inn check the difference in each quater and in each year.

8. Setup streamlit homepage with 4 sidebar items and each have 2 tabs except the homepage.

## Conclution:

I have given the source code and the required files in this repository to everyone to try this our,
Streamlit is a cool and easy to use app with litrally no html and css coding. 

With this we can get the insights of how user anre there and how much amount transfered and which state is in top of the transactions like that.

## THANK YOU!!!!
