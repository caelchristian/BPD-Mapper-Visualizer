import sqlite3
import os
import pandas as pd
from pathlib import Path
import sys

def load_csv(filename, table_name):
    """Takes CSV files and loads them onto a SQLite database
    Args:
        filename (string): Local dir of .csv file (data/...)
    """
    # check if csv file exists
    if not (os.path.isfile(filename)):
        print(str(filename) + " file does not exist!")
        # check if csv is empty
    if (os.path.getsize(filename) == 0):
        print(str(filename) + " file is empty! Cannot load empty dataset into a database.")
    else:
        # if database file has not been loaded/created, create DB file
        if not (os.path.isfile("instance/credentials.db")):
            # create a database file if one does not exist already
            Path('instance.credentials.db').touch()
        
        try:
            # create connections to instance/credentials.db
            # cursor is used to load data.
            # if db file doesn't exist, it is created
            connection = sqlite3.connect('instance/credentials.db')
            cursor = connection.cursor()
            
            # load dataset into a Pandas DataFrame
            dataset = pd.read_csv(filename)
            
            dataset.to_sql(table_name, connection, if_exists='replace', index = False)
            
            # save changes
            connection.commit()
            
            print("Dataset has been loaded into \"instance/credentials.db\".\n")
            return True
        
        except BaseException as e:
            print("Connection could not be made to database file. Dataset could not be loaded. Error:", e)
            return False
        
        # close connections
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
                
def main():
    load_csv("final/data/Police_Arrests.csv", "Arrests")
    load_csv("final/data/Police_Incidents.csv", "Incidents")
    load_csv("final/data/Traffic_Stops.csv", "Stops")
    
if __name__ == "__main__":
    main()