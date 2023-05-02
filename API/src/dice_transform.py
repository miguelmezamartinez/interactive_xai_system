import json
from database_req import create_connection, get_application
from constants import feature_names_model_ordered, rename_dict
from models import DiceCounterfactualResponse, InstanceInfo, ModelInstanceInfo

ordered_attribute_model = [rename_dict[feature_names_model_ordered[i]] for i in range(18)]
reorder = [0,1,2,3,4,5,6,7,9,10,11,12,13,14,15,8,16,17]
tmp_ordered_list = [ordered_attribute_model[i] for i in reorder]
ordered_attribute_model = tmp_ordered_list


final_cf_dict = {}

with open("Data/all_counterfactuals.json", "r") as f:
    cfs = json.load(f)

    for i in range(1000):
        current_instance = get_application(create_connection("database.db"), i, True)
        
        list_of_cfs = []
        for li in cfs[str(i)]: # for all 5 counterfactuals
            tmp_cf = {ordered_attribute_model[i] : li[i] for i in range(len(ordered_attribute_model))} # map the cf values to their attribute name
            for key in ordered_attribute_model:
                if tmp_cf[key] == current_instance[key]: # remove value from cf if it is the same in the original instance
                    tmp_cf.pop(key)
            list_of_cfs.append(tmp_cf)

        instance_dice_response = {"original_instance": current_instance, "counterfactuals":list_of_cfs}
        final_cf_dict[i] = instance_dice_response

with open("Data/cfs_response_format.json", "w") as file:
    json.dump(final_cf_dict, file)


