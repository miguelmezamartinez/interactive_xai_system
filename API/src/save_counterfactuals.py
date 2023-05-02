from time import time
import dice_ml
import pandas as pd
from tensorflow.python.keras.saving.save import load_model
from DataLoader_ey import data_loader
import tensorflow as tf
import json

def process_instance(query_instance, exp):
    dice_exp = exp.generate_counterfactuals(query_instance, total_CFs=5, desired_class="opposite", posthoc_sparsity_algorithm="binary")
    cf_result = json.loads(dice_exp.to_json())['cfs_list']
    return cf_result

def iterate_instances(start, num_instances, data: pd.DataFrame, exp, queue, no_queue=False):
    result = {}
    import time
    for i in range(start, start + num_instances):
        instance = data.iloc[i, :].to_dict()
        result[i] = process_instance(instance, exp)
        print("Sleeping 5 seconds to cool down!")
        time.sleep(5)
    
    if no_queue:
        return result

    queue.put(result)

def cf_gen_worker(start, num_instances):
    data = data_loader("Data/german.csv")
    backend = 'TF2'
    model = load_model('smote_ey.tf')
    d = dice_ml.Data(dataframe=data, continuous_features=['duration_', 'amount_', 'age_'], outcome_name='label')
    d.normalize_data(d.one_hot_encode_data(data))
    m = dice_ml.Model(model=model, backend=backend)
    exp = dice_ml.Dice(d, m)
    res = iterate_instances(start, num_instances, data, exp, queue=None, no_queue=True)
    print(f"INFO: Succesfully generated counterfactuals for {num_instances} instances!")
    with open(f"test_res_{start}_{num_instances}.json", "w") as file:
        json.dump(res, file)



if __name__ == "__main__":
    # Some cfs take 3 minutes to load, which means this could take a very huge amount of time...
    m_processes = 4
    instances_per_process = 2

    import multiprocessing as mp

    processes = [mp.Process(target=cf_gen_worker, args=(i*instances_per_process, instances_per_process, )) for i in range(m_processes)]
    for p in processes:
        print("process started!")
        p.start()

    for p in processes:
        p.join()

    print(f"finished generating counterfactuals for {m_processes*instances_per_process} instances!")