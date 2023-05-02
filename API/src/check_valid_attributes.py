# This script is not necessary for the application
# It is only used to test wether all defined model attributes are correctly specified.
import json
from constants import rename_dict, inv_rename, feature_names_model_ordered, attribute_constraints
import requests

# baseline request for the model
baseline_req_api = {
  "balance": "string",
  "duration": 0,
  "history": "string",
  "purpose": "string",
  "amount": 0,
  "savings": "string",
  "employment": "string",
  "available_income": "string",
  "residence": "string",
  "assets": "string",
  "age": 0,
  "other_loans": "string",
  "housing": "string",
  "previous_loans": "string",
  "job": "string",
  "other_debtors": "string",
  "people_liable": "string",
  "telephone": "string"
}

baseline_value = 0.5808144807815552

baseline_model = {k : baseline_req_api[rename_dict[k]] for k in feature_names_model_ordered}

# print("baseline request:\n", str(baseline_req_api))
# print(baseline_model)

r = requests.post("http://localhost:8000/instance/predict", json=baseline_req_api)
assert r.json()["NN_recommendation"] == "Reject" and r.json()["NN_confidence"] == baseline_value

# Now, change the value for each attribute individually, to see if it changes something in the models output. If it does, the attributevalue is correctly specified

faulty_values = {}

# Check values for each categorical constraint
for constraint in attribute_constraints:
    if constraint["type"] == "continuous" or "NN" in constraint["attribute"].value:
        continue # skip anything that isn't continuous or does not have anything to do with 
    attr_name = constraint["attribute"].value
    attr_values = constraint["values"]
    faulty_list = []
    print(f"\033[92mINFO:\033[0m checking {attr_name} for model misbehaving.")
    for val in attr_values: # check every specified value
        print(f"    checking {val}")
        tmp = baseline_req_api.copy()
        tmp[attr_name] = val # only change one value, to see if the prediction changes. If it does, then the value is correctly specified
        tmp_r = requests.post("http://localhost:8000/instance/predict", json=tmp)
        try:
            assert not (tmp_r.json()["NN_recommendation"] == "Reject" and tmp_r.json()["NN_confidence"] == baseline_value)
        except AssertionError: 
            # gets executed when the value didn't change the prediction, which means that the model does not know the value and has no encoding for it
            print(f"    \033[91mWARNING\033[0m: {val} is wrongly specified for attribute {attr_name}")
            faulty_list.append(val)
    if len(faulty_list) > 0:
        faulty_values[attr_name] = faulty_list

print(faulty_values)