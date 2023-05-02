import sqlite3 as sql
import json
from typing import List
import pandas as pd
from models import ExperimentResults

from constants import *


def create_connection(db: str):
    """ Builds a connection to the database stored in the given file db and returns the connection element."""
    con = None
    try:
        con = sql.connect(db)
    except sql.Error as e:
        print(e)
    return con


def get_applications(con, start: int, num=20):
    """Returns the applications with the ids from start to start + num
    Needs a connection con to the database.db (use create_connection) and a start value as int """
    c = con.cursor()
    end = int(start) + int(num)
    query = f'SELECT * FROM applicants WHERE ident >= {start} AND ident < {end}'
    c.execute(query)
    result = c.fetchall()
    return result


def get_application(con, ident: int, json_str=False):
    """Returns the application information for the application with the specified id.
    Needs a connection con to the database and the id.
    Result can be returned in json format."""
    if json_str:
        con.row_factory = sql.Row
    c = con.cursor()
    query = f'SELECT * FROM applicants WHERE id = {ident}'
    rows = c.execute(query).fetchall()
    if json_str:
        for ix in rows:
            json_dump = json.dumps(dict(ix))
    result = json.loads(json_dump)
    return result


def get_applications_custom(con, start: int, attributes: List[str],  num=20, json_str=False, filters=None, sort="ident", sort_asc=True):
    """Returns a list of application data from the database that is connected via con. 
    Attributes is the list of chosen attributes, num the amount of applications that is requested, 
    filters a list of jsons with filter information, sort a String of the attribute name to be sorted by sort_desc allows to sort by descending order.
    Result can also be returned in json format."""
    if json_str:
        con.row_factory = sql.Row
    c = con.cursor()
    view_query = 'CREATE VIEW custom AS '
    # add customize values
    chosen = AttributeNames.ident.value
    if len(attributes) > 0:
        chosen += ','
        for i in range(0, len(attributes)):
            chosen += str(attributes[i])
            chosen += ','
        chosen = chosen[:-1]
    view_query += 'SELECT Row_Number() OVER '
    view_query += create_order_query(sort)
    if sort_asc == False:
        view_query += ' DESC'
    view_query += f') RowNum,{chosen} FROM applicants'
    # add filters to query
    if filters:
        view_query += create_filter_query(filters)
    c.execute(view_query)
    con.commit()
    end = start + num
    query = f'SELECT {chosen} FROM custom WHERE RowNum > {start} AND RowNum <= {end}'
    rows = c.execute(query).fetchall()
    c.execute("DROP VIEW custom")
    con.commit()
    if json_str:
        rows = json.dumps([dict(ix) for ix in rows])
        rows = json.loads(rows)
    return rows


def create_filter_query(filters):
    """Creates a string for the filter query in sql from a given list of filters in json format."""
    filter_str = " WHERE "
    for i in range(0, len(filters)):
        filter_dict = vars(filters[i])
        attribute = filter_dict[attr_name_abr]
        if (values in filter_dict):
            # categorical filter
            selected = filter_dict[values]
            filter_str += "("
            for j in range(0, len(selected)):
                filter_str += f"{attribute} = '{selected[j]}'"
                if j < len(selected) - 1:
                    filter_str += " OR "
            filter_str += ")"
        else:
            # numerical
            filter_str += f"({attribute} >= {filter_dict[lower_bound]} AND {attribute} <= {filter_dict[upper_bound]})"
        if i < len(filters) - 1:
            filter_str += " AND "
    return filter_str


def create_order_query(sort: str):
    """Creates a string for the ordering query in sql for a given attribute name as a string"""
    query = '(ORDER BY '
    attr_dict = {}
    if (sort == AttributeNames.ident.value):
        query += sort
        return query
    for constraint in attribute_constraints:
        if constraint[attr_name] == sort:
            attr_dict = constraint
            break
    if (attr_dict[const_type] == categorical):
        query += 'CASE'
        count = 1
        for entry in attr_dict[values]:
            query += f" WHEN {sort} = '{entry}' THEN {count}"
            count += 1
        query += ' END'
    else:
        query += sort
    return query


# for create_experiment
def exp_creation(con, exp_name: str, exp_info: str):
    """Checks if the experiment already exists in the database and adds it to the experiments table if not."""
    exp_name = exp_name.replace("'", "''")
    if not check_exp_exists(con, exp_name):
        c = con.cursor()
        # single quotes need to be replaced with double single quotes as otherwise sql assumes it indicates the end of a string
        exp_info = exp_info.replace("'", "''")
        insert_query = f"INSERT INTO experiments (name, information) VALUES ('{exp_name}','{exp_info}')"
        c.execute(insert_query)
        con.commit()


# for experiment_list
def get_all_exp(con):
    """Returns a list of all experiments"""
    query = "SELECT name FROM experiments"
    c = con.cursor()
    results = c.execute(query).fetchall()
    res_list = []
    for result in results:
        # index 0 needed because result is in a tuple format
        res_list.append(result[0])
    return res_list

# for experiment_by_name


def get_exp_info(con, name: str):
    """If the given experiment is in the database the corresponding experiment information is returned in 
    json format."""
    name = name.replace("'", "''")
    query = f"SELECT information FROM experiments WHERE name = '{name}'"
    c = con.cursor()
    results = c.execute(query).fetchall()
    if len(results) == 0:
        return {}
    result_tuple = results[0]
    result_str = result_tuple[0]
    result_json = json.loads(result_str)
    participants_query = f"SELECT * FROM results WHERE experiment_name = '{name}' AND results != 'NULL'"
    participants = c.execute(participants_query).fetchall()
    number_participants = len(participants)
    result_json["num_participants"] = number_participants
    return result_json

# for generate_clientID


def create_id(con, exp_name: str):
    """Queries the database for already existing ids for that experiment and chooses the lowest available id.
    For this id and the experiment name an entry in the results table is created, where later the results can be added.
    :returns: json with key client_id and the newly generated id or None if the experiment does not exist"""
    exp_name = exp_name.replace("'", "''")
    if check_exp_exists(con, exp_name):
        query_existing_id = f"SELECT client_id FROM results WHERE experiment_name = '{exp_name}'"
        c = con.cursor()
        ids = c.execute(query_existing_id).fetchall()
        if len(ids) > 0:
            # makes sure there is no id with higher value, max also works with single valued tuples
            return_id = max(ids)[0] + 1
        else:
            return_id = 0
        query_insert = f"INSERT INTO results (experiment_name, client_id, results) VALUES('{exp_name}',{return_id}, NULL)"
        c.execute(query_insert)
        con.commit()
        return_dict = {
            client_id: return_id
        }
        return return_dict


# for results to database
def add_res(con, exp_name: str, client_id: int, results: List[ExperimentResults.SingleResult]):
    """Adds the given results to the experiment name and client id in the results table."""
    dict = {}
    for res in results:
        dict[res.loan_id] = res.json()
    # get json for the results list, as sqllite cannot save lists
    json_str = json.dumps(dict)
    exp_name = exp_name.replace("'", "''")
    query = f"UPDATE results SET results = '{json_str}' WHERE experiment_name = '{exp_name}' AND client_id = {client_id}"
    c = con.cursor()
    c.execute(query)
    con.commit()


# export results
def export_results_to(con, format, exp_name=None):
    """Returns the experiment results. If an exp_name is given, only the results for that experiment are returned
    and it is possible to choose between csv and json format. If no exp_name is given, the result is returned in json format."""
    query = "SELECT * FROM results WHERE results != 'NULL'"
    if exp_name:
        exp_name = exp_name.replace("'", "''")
        query += f" AND experiment_name =  '{exp_name}'"
    con.row_factory = sql.Row
    c = con.cursor()
    results = c.execute(query).fetchall()
    if results == []:
        if format == ExportFormat.comma_separated.value:
            df = pd.DataFrame()
            df.to_csv(csv_path)
            return csv_path
        else:
            return []
    result = json.dumps([dict(res) for res in results])
    result_json = json.loads(result)
    for res in result_json:
        results_list = []
        results = json.loads(res[results_key])
        for key in results.keys():
            results_list.append(json.loads(results[key]))
            res[results_key] = results_list
    if format == ExportFormat.comma_separated.value:
        df = pd.DataFrame(result_json)
        results = df[results_key]
        first_results = df.loc[0, results_key]
        list_dict = {}
        for decision in first_results:
            list_dict[decision[loan_id]] = []
        for res in results:
            for decision in res:
                list_dict[decision[loan_id]].append(decision[choice])
        for key in list_dict.keys():
            df[str(key)] = list_dict[key]
        df = df.drop(columns=results_key)
        df.to_csv(csv_path, index=False)
        return csv_path
    return result_json


# for reset_experiment_results
def reset_exp_res(con, exp_name: str):
    """Deletes all results for an experiment with the given name from the results table."""
    exp_name.replace("'", "''")
    reset_query = f"DELETE FROM results WHERE experiment_name = '{exp_name}'"
    c = con.cursor()
    c.execute(reset_query)
    con.commit()

# for delete_experiment


def delete_exp(con, exp_name: str):
    """Checks if the experiment exists and deletes it from the experiments table if yes."""
    exp_name = exp_name.replace("'", "''")
    if check_exp_exists(con, exp_name):
        c = con.cursor()
        delete_query_exp = f"DELETE FROM experiments WHERE name = '{exp_name}'"
        c.execute(delete_query_exp)
        delete_query_res = f"DELETE FROM results WHERE experiment_name ='{exp_name}'"
        c.execute(delete_query_res)
        con.commit()


def cf_response_format_db(con, path: str):
    """Reading counterfactuals stored in a json from the given path, formatting them and adding them to the database."""
    c = con.cursor()
    with open(path, 'r') as file:
        cfs = json.load(file)
    for key in cfs.keys():
        instance = cfs[key]
        cf = instance[counterfactuals]
        cf_dict = {}
        cf_dict[counterfactuals] = cf
        query = f"INSERT INTO dice (instance_id, counterfactuals) VALUES({key}, '{json.dumps(cf_dict)}');"
        c.execute(query)
    con.commit()


def get_cf(con, instance_id: int):
    """For that instance id the pregenerated counterfactuals are returned from the dice table if the id is
    between 0 and 999."""
    if instance_id in range(number_of_applications):
        query = f"SELECT counterfactuals FROM dice WHERE instance_id = {instance_id}"
        c = con.cursor()
        results = c.execute(query).fetchall()
        result = results[0]
        res_str = result[0]
        res_json = json.loads(res_str)
        return res_json


def check_exp_exists(con, exp_name: str):
    """Checks whether or not an experiment with the given name exists in the table `experiments`. Returns true if it exists."""
    exists_query = f"SELECT name FROM experiments WHERE name = '{exp_name}'"
    query_res = con.execute(exists_query).fetchall()
    if len(query_res) > 0:
        return True
    return False
