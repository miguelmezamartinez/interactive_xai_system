
from turtle import resetscreen
from matplotlib.font_manager import json_load
from database_req import *
import json
from models import ExperimentInformation
import models

con = create_connection('database.db')
query = "SELECT information FROM experiments WHERE name = 'string'"
c = con.cursor()
results = c.execute(query).fetchall()
result_tuple = results[0]
result_str = result_tuple[0]
print(result_str)
result_json_str = json.dumps(result_str)
result_json = json.loads(result_str)
print(result_json["loan_ids"])


'''
con = create_connection('database.db')
exp_info_dict = {
    'loan_ids' : [1,2,3,4,5],
    'ismodify' : True,
    'iswhatif' : True, # Should only be True if ismodify is also true
    'exp_type' : 'shap',
    'experiment_name' : 'Test experiment'
}
json1 = json.dumps(exp_info_dict)
json_obj = json.loads(json1)
#exp_creation(con, 'Test experiment', json_obj)

exp_info_dict2 = {
    "loan_ids" : [1,2,7,4,5],
    "ismodify" : True,
    "iswhatif" : False, # Should only be True if ismodify is also true
    "exp_type" : "shap",
    "experiment_name" : "Test experiment 2"
}
json12 = json.dumps(exp_info_dict2)
json_obj2 = json.loads(json12)

#exp_creation(con, 'Test experiment 2', json_obj2)
#res = get_exp_info(con, 'Test experiment 2')
#res = get_all_exp(con)


str_repr = {
    "loan_ids": [1, 2, 7, 4, 5], 
    "ismodify": True, 
    "iswhatif": False, 
    "exp_type": "shap", 
    "experiment_name": "Test experiment 2"
}
j1 = json.dumps(str_repr)
j2 = json.loads(j1)
#delete_exp(con, 'Test experiment')

#res = get_application(con, 0)
l = ["balance", "duration", "history", "amount"]
#res = get_applications_custom(con, 0, l)
balance_dict = {
    "attribute": "balance",
    "values": ["no balance", "no account"]
}
amount_dict = {
    "attribute": "amount",
    "lower_bound": 0,
    "upper_bound": 10000
}
filter1 = json.dumps(balance_dict)
filter2 = json.dumps(amount_dict)
jsonobject = json.loads(filter2)
#print(jsonobject.type())
filters = [filter1, filter2]
#res = get_applications_custom(con, 0, l, sort='id')
res = get_application(con, 1, json_str=True)
#res = res[1:-1]
print(res)
'''
