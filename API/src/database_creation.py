from DataLoader_ey import createDataframeForDB
import sqlite3 as sql
from constants import *
from database_req import cf_response_format_db 

"""This script can be run to create the database needed for the program.
It creates the four tables applicants, dice, experiments and results.
The applicants table is initialised with the loan applications from the german.csv data.
The dice table is initialised with the pregenerated counterfactuals from cfs_response_format.json.
The experiments table is used to store experiment information and the results table for the experiment results.
"""

con = sql.connect(db_path)
c = con.cursor()
#the create_query is only needed for initialisation not when just wanting to reset
create_query_appl ='CREATE TABLE IF NOT EXISTS applicants (id INT, balance TEXT,duration INT,history TEXT,purpose TEXT,amount REAL,savings TEXT,employment TEXT,available_income TEXT,other_debtors TEXT,residence TEXT,assets TEXT,age INT,other_loans TEXT,housing TEXT,previous_loans TEXT,job TEXT,people_liable TEXT,telephone TEXT, NN_recommendation TEXT, NN_confidence REAL)'
c.execute(create_query_appl)
con.commit()
df = createDataframeForDB()
df.to_sql('applicants', con, index_label = 'id', if_exists="replace")
for key in rename_dict.keys():
    query = 'ALTER TABLE applicants RENAME COLUMN ' + key + ' TO ' + rename_dict[key] + ';'
    c.execute(query)
create_query_exp = 'CREATE TABLE IF NOT EXISTS experiments (name TEXT PRIMARY KEY, information TEXT);'
c.execute(create_query_exp)
con.commit()
create_query_res = 'CREATE TABLE IF NOT EXISTS results (experiment_name TEXT REFERENCES experiments (name) ON DELETE CASCADE ON UPDATE CASCADE, client_id INT, results JSON, PRIMARY KEY (experiment_name, client_id));'
c.execute(create_query_res)
create_query_cf = 'CREATE TABLE IF NOT EXISTS dice (instance_id INT PRIMARY KEY REFERENCES applicants (id) ON DELETE CASCADE ON UPDATE CASCADE , counterfactuals JSON);'
c.execute(create_query_cf)
con.commit()
cf_response_format_db(con, 'Data/cfs_response_format.json')
con.close()
