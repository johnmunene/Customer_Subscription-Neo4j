# Customer_Subscription-Neo4j

This program is a pipeline that utilizes the power of neo4j graphical data storage, python and postgress.
As a prerequisite stage, customer data is imported into neo4j and relations created.
The programs has several functions to retrieve the dat from neo4j database process it and load it to postgress.
The extract function access the cloud based neo4j and extracts the data which is then converted into a dataframe.
The tranform function used pandas library to clean and tranform the data.
The load function uses the psycopg2 to load data into postgres SQL
