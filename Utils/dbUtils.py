import mysql.connector as mysqlConnector
from Configs.dbConfigs import CHECK_IF_EXISTS_IN_BULK, HOST_NAME, DB_NAME, DB_USER_NAME, PORT_NAME, DB_PASSWORD, CHECK_IF_EXISTS, SEARCH_QUERY
from Configs.envrinomentSpecificConfgis import TABLE_NAME
import os
import datetime
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

# RETURN ERROR DETAILS STRING FOR LOGGING
def get_sql_connector():
    return mysqlConnector.connect(
        host=HOST_NAME,
        user=DB_USER_NAME,
        passwd=DB_PASSWORD,
        database=DB_NAME,
        port=PORT_NAME
    )

def getErrorDetails(errorObject):
    return "{} \n {} \n {} \n {}".format(
        "Exception Occurred while Operating on Database: {}".format(
            errorObject),
        "Error Code: {}".format(errorObject.errno),
        "SQL_STATE: {}".format(errorObject.sqlstate),
        "Error Message: {}".format(errorObject.msg)
    )

# EXECUTE INSERT COMMAND
def executeCommand(command):
    # Open SQL Connection
    sqlConnector = get_sql_connector()

    mySQLCursor = sqlConnector.cursor()

    try:
        # Execute Command
        mySQLCursor.execute(command)

        # Insert into DB
        sqlConnector.commit()

    except mysqlConnector.Error as err:
        print(getErrorDetails(err))

    # Close the Connection
    mySQLCursor.close()
    sqlConnector.close()


def execute_insert_command(command, vals):
    # Open SQL Connection
    sqlConnector = get_sql_connector()

    mySQLCursor = sqlConnector.cursor()
    try:
        
        mySQLCursor.execute(CHECK_IF_EXISTS.format(TABLE_NAME), (vals[2],))
        result = mySQLCursor.fetchone()[0]
        if result == 0:
            mySQLCursor.execute(command, vals)

            # Insert into DB
            sqlConnector.commit()
            # print("Inserted!!")
        else:
            # pass
            print(f"Record with public_urn: {vals[2]} already exists, skipping!")
        
    except mysqlConnector.Error as err:
        print(command)
        print(getErrorDetails(err))

    # Close the Connection
    mySQLCursor.close()
    sqlConnector.close()

# EXECUTE GET COMMAND
def execute_get_command(command):
    # Open SQL Connection
    returnOneRow = None
    
    sqlConnector = get_sql_connector()

    mySQLCursor = sqlConnector.cursor()

    try:
        # Execute Command
        mySQLCursor.execute(command)

        # Fetch from Table and return one Row
        returnOneRow = mySQLCursor.fetchall()

    except mysqlConnector.Error as err:
        print(getErrorDetails(err))

    # Close the Connection
    mySQLCursor.close()
    sqlConnector.close()

    # Return one Row
    return returnOneRow

def check_if_entry_exists_in_db(query, sqlConnector):
    mySQLCursor = sqlConnector.cursor()

    mySQLCursor.execute(query)
    exists = mySQLCursor.fetchone()
    mySQLCursor.close()
    sqlConnector.close()

    if exists:
        return True
    return False

def readSQLQueryinPD(command):
# Connect to the database
    sqlConnector =get_sql_connector()

    # Read the query results into a pandas DataFrame
    df = pd.read_sql_query(command, con=sqlConnector)

    sqlConnector.close()

    return df

def insert_bulk_data(data, query):
    
    profile_urn_id_list = data['profile_urn_id'].tolist()


    # Connect to the database
    sqlConnector = get_sql_connector()
    cursor = sqlConnector.cursor()

    query_to_check_if_exists_in_bulk = CHECK_IF_EXISTS_IN_BULK.format(TABLE_NAME, ",".join(["%s"] * len(profile_urn_id_list)))
    cursor.execute(query_to_check_if_exists_in_bulk, tuple(profile_urn_id_list))

    # Fetch the results
    existing_urn_ids = [result[0] for result in cursor.fetchall()]

    # Filter the DataFrame to retain only rows with non-existing profile_urn_ids
    filtered_data = data[~data['profile_urn_id'].isin(existing_urn_ids)]


    # Fetch existing URN IDs from the database
    # Convert the filtered DataFrame to a list of tuples
    data_to_insert = filtered_data.to_records(index=False).tolist()
    
    # Perform bulk insertion
    try:
        cursor.executemany(query, data_to_insert)
        sqlConnector.commit()
    except Exception as e:
        print(getErrorDetails(e))
    finally:  
        # Close the database connection
        cursor.close()
        sqlConnector.close()