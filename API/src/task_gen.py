from queue import Queue
import threading
from pydantic import BaseModel, Field
from models import ShapResponse, LimeResponse
from shap_utils import compute_response_shap
from constants import ResponseStatus, ExplanationType, all_features, timeout_seconds
from typing import Optional
from uuid import UUID, uuid4
import time

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

class Job(BaseModel):
    exp_type : ExplanationType
    uid : UUID = Field(default_factory=uuid4)
    task : dict = {} # instance attributes with values & arguments necessary for computation
    status : str = Field(ResponseStatus)

def explanation_worker(in_queue : Queue, res_out : dict):
    """Takes one element (a job) out of the input queue (TODO BLOCKING), solves the task
    with the explanation function which takes in the args.
    The result is returned in the output queue.
    
    Params:
    -------
    :param in_queue: the multiprocessing.Manager Queue used for shared memory between processes. Tasks are in here.
    :param res_out: the Manager dict used to store the results of the computations with respect to the Job uuid

    TODO """
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
    # imports for explainers
    # Need to happen in the worker, because pickle can't serialize the necessary objects for child processes

    #Shap
    import shap
    from shap_utils import ShapHelperV2
    sh = ShapHelperV2()
    sh.prepare_shap()
    pred_fn = sh.predict_shap


    shap_explainer = shap.KernelExplainer(pred_fn, sh.X_train)
    cols = sh.X_train.columns.to_list()

    #Lime
    from lime_utils import LimeHelper
    lh = LimeHelper()

    print(f"\033[92mINFO:\033[0m Explainer process with id \033[96m{os.getpid()}\033[0m started succesfully. Explainers loaded and ready.")
    
    while True: # repeat the process
        print(f"\033[92mINFO:\033[0m Explainer process with id \033[96m{os.getpid()}\033[0m is waiting for the next task.")
        job : Job = in_queue.get(block=True) # explicitely wait until a job is available
        start_time = time.time()
        print(f"\033[92mINFO:\033[0m Explainer process with id \033[96m{os.getpid()}\033[0m starting exlanation computation. \
            \n      Explanation type: \033[1m{job.exp_type.value}\033[0m")


        if job.exp_type in [ExplanationType.shap, ExplanationType.shap_orig]:
            # Modification Backup
            # Add sh to parameter to compute prediction
            #shap_bval, shap_vals, pred_proba, recommendation  = compute_response_shap(job.task["instance"], shap_explainer, cols, sh)
            shap_bval, shap_vals, = compute_response_shap(job.task["instance"], shap_explainer, cols)

            shap_attributes = [{"attribute" : cols[i], "influence" : shap_vals[0][i]} for i in range(len(cols))] # prepare format for response

            #out = ShapResponse(status=ResponseStatus.terminated, base_value=shap_bval, values=shap_attributes, pred_proba=pred_proba, recommendation=recommendation)
            out = ShapResponse(status=ResponseStatus.terminated, base_value=shap_bval, values=shap_attributes)
            res_out[job.uid] = out
        elif job.exp_type in [ExplanationType.lime, ExplanationType.lime_orig]:
            if job.task["num_features"] is not None:
                num_features = job.task["num_features"]
            else:
                num_features = all_features
            # Modification
            # Add base value
            lime_vals, lime_bval = lh.compute_response_lime(job.task["instance"].__dict__, num_features) #pass the instance in the required format
            #lh_res = lh.compute_response_lime(job.task["instance"].__dict__, num_features) #pass the instance in the required format
            out = LimeResponse(status=ResponseStatus.terminated, base_value=lime_bval, values=lime_vals)
            #out = lh_res
            #res_out[job.uid] = LimeResponse(status=ResponseStatus.terminated, values=lh_res)
            res_out[job.uid] = out
        else:
            print(f"\033[93mWARNING:\033[0m \033[1m{job.exp_type.value}\033[0m is invalid for explanation with uuid {job.uid}. Fetching new job.")
            continue

        end_time = time.time()

        print(f"\033[92mINFO:\033[0m Explainer process with id \033[96m{os.getpid()}\033[0m finished \033[1m{job.exp_type.value}\033[0m computation.\n      Time taken: {end_time-start_time} seconds.")
        print(f"      Result saved with uuid {job.uid}.")

        threading.Thread(target=timeout_explanation, args=(job.uid, res_out, timeout_seconds)).start()
        print(f"      Timeout for explanation {job.uid} has begun. Deletion in {timeout_seconds} seconds.")


def timeout_explanation(uid: UUID, results_dict: dict, timeout_seconds: int):
    '''Will remove the generated explanation a certain amount of time after its generation. This method should only be used after the explanation has been generated.'''
    time.sleep(timeout_seconds)
    try:
        results_dict.pop(uid)
    except KeyError:
        # Could have been deleted otherwise
        print(f"\033[92mINFO:\033[0m Explanation with uuid {uid} couldn't be deleted. Key does not exist.")

    print(f"\033[92mINFO:\033[0m Explanation with uuid {uid} has been deleted due to timeout.")   