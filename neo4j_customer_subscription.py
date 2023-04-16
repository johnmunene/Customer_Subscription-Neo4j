#!/usr/bin/env python
# coding: utf-8

# In[315]:


# Import required libraries
from neo4j import GraphDatabase
import pandas as pd
import psycopg2


# Define Neo4j connection details
bolt_url = "neo4j+s://12aac262.databases.neo4j.io"
user = "neo4j"
password = "kYF39qIW49v5QsREyGDbtb11N3KY_3EVMB0U5qSNiI8"

# Define Postgres connection details
pg_host = 'localhost'
pg_database = 'Customer_Subscription'
pg_user = 'postgres'
pg_password = 'Nevergiveup.1'

# Define Neo4j query to extract data
ql ='''

MATCH (Customer_ID)-[:subscription]->(Subscription_ID)-[:Service]->(Service_ID)-[:start]->(Start)-[:End]->(End)-[:price]->(Price) RETURN Customer_ID, Subscription_ID, Service_ID, Start, End, Price LIMIT 500
'''

# Define function to extract data from Neo4j and return a Pandas DataFrame
def extract_data():
    # Connect to Neo4j
    driver = GraphDatabase.driver(bolt_url, auth=(user, password))
    #Create session
    session = driver.session()
    #run seesion to querry data
    results = session.run(ql)
    data = results.data()
    #convert the data to dataframe
    df = pd.DataFrame(data)
    
    
    return df


# Define function to transform data
def transform_data(df):
    
    #conver the df data to usable data frame
    for i in range (len(df['Customer_ID'])):
        df['Customer_ID'][i] = df['Customer_ID'][i]['Customer_ID']
    for j in range (len(df['Subscription_ID'])):
        df['Subscription_ID'][j] = df['Subscription_ID'][j]['Subscription_ID']
    for k in range (len(df['Service_ID'])):
        df['Service_ID'][k] = df['Service_ID'][k]['Service_ID']
    for l in range (len(df['Start'])):
        df['Start'][l] = df['Start'][l]['Start_date_of_subscription']
    for m in range (len(df['End'])):
        df['End'][m] = df['End'][m]['End_date_of_subscription']
    for n in range (len(df['Price'])):
        df['Price'][n] = df['Price'][n]['Price_of_subscription']
        
   
    
    
    # Remove null values
    df1 = df.dropna()
    #remove repetitive data
    df1['Customer_ID'] = df1['Customer_ID'].str.replace('C', '')
    df1['Subscription_ID'] = df1['Subscription_ID'].str.replace('prd_', '')
    df1['Service_ID'] = df1['Service_ID'].str.replace('CC', '')
    
    #rename columns
    df1.rename(columns = {'Start':'Start_of_Subscription', 'End':'End_of_Subscription'}, inplace = True)
    df2 = df1.astype({'Customer_ID':'int','Subscription_ID':'int', 'Price':'float','Service_ID':'int'})
    
        
    return df2

# Define function to load data into Postgres
def load_data(df2):
    # Connect to Postgres
    conn = psycopg2.connect(host=pg_host, database=pg_database, user=pg_user, password=pg_password)
    
    # Create a cursor object
    cur = conn.cursor()

    # Create a table to store the data
    cur.execute('CREATE TABLE IF NOT EXISTS Customer_Subscription (\
                 Customer_ID INT,\
                 Subscription_ID INT,\
                 Service_ID INT,\
                 Start_of_Subscription DATE,\
                 End_of_Subscription DATE,\
                 Price FLOAT\
                 )')

    # Insert the transformed data into the database
    for i, row in df2.iterrows():
        cur.execute(f"INSERT INTO Customer_Subscription (Customer_ID, Subscription_ID, Service_ID, Start_of_Subscription, End_of_Subscription, Price) VALUES ({row['Customer_ID']}, {row['Subscription_ID']}, '{row['Service_ID']}', '{row['Start_of_Subscription']}', '{row['End_of_Subscription']}', {row['Price']})")

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

# Define main function
def main():
     #Extract data from Neo4j
    df = extract_data()
    # Transform data using Pandas
    df2 = transform_data(df)
      # Load data into Postgres
    load_data(df2)
   
    
    
    
  
    

# Call main function
if __name__ == "__main__":
    main()

