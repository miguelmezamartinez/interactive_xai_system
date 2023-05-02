import os
import uvicorn
import multiprocessing as mp
from tensorflow.keras.models import load_model
import pandas as pd
import pickle
import psutil
import hashlib

from starlette.status import HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from starlette.background import BackgroundTask
import json

from typing import Any, Optional, List, Union
from fastapi import FastAPI, Query, HTTPException
from fastapi.params import Body
from fastapi.responses import FileResponse
from task_gen import explanation_worker
from task_gen import Job
from typing import Dict
from uuid import UUID
from constants import *
from models import *
from fastapi.middleware.cors import CORSMiddleware
from database_req import *

API_description = '''
# TSE: Explainable Artificial Intelligence - API
## Developers: Isabelle Konrad, Felix Hasse, Nicolas Kiefer, Tilio Schulze & Miguel Angel Meza Martínez
___
### API: JSON key naming
To change the key names, go to the file `constants.py`. This API uses the defined strings in
`constants.py` as key aliases. All the `pydantic` models conform to using `pydantic.Field` with the constant strings
as the public aliases. This leads to a better separation between the python naming norms and the API key names.
'''

tags_metadata = [
    {
        "name": "Dataset",
        "description": "All requests related to the 'German Credit Dataset' and the tensorflow model for binary classification."
    },
    {
        "name": "Explanations",
        "description": "All requests using XAI methods."
    },
    {
        "name": "Debugging",
        "description": "Requests for debugging possibilities. Include basic diagnostics about all running processes."
    },
    {
        "name": "Experimentation",
        "description": "All requests related to XAI experimentation functionalities."
    }
]

app = FastAPI(description=API_description, openapi_tags=tags_metadata)

manager = None
num_processes = None
process_ids = []
task_queue = None  # tasks will be inputted here
results: Dict[UUID, Any] = {}  # finished tasks will be inputted here
#os.chdir("c:/Users/D073188/Documents/GitHub/Interactive_xai/API/src")
tf_model = load_model("./smote_ey.tf")

# hash for admin password, not secure, idea is only to
admin_pwd_hash = '5adfb2c0eca0935eede2af480a5d60b7481ee308ef8c0a14b4e0d367067d8842'

# This preprocessor was pickled in python 3.8.12.
# It follows the steps from data_loader_ey, except that the preprocessor is returned
preprocessor = pickle.load(open("preproc.pickle", "rb"))

# This is necessary for allowing access to the API from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# api requests start here


# second parameter makes sure that unused stuff won't be included in the response
@app.post("/table", response_model=List[InstanceInfo], response_model_exclude_none=True, tags=["Dataset"])
async def table_view(request: TableRequest):
    '''Returns a list of "limit" instances for the table view from a specific offset. Can have filters and chosen attributes, aswell as sorting.'''
    con = create_connection(db_path)
    attributes = []
    for i in request.attributes:
        attributes.append(i.value)
    attributes.append(AttributeNames.NN_recommendation.value)
    attributes.append(AttributeNames.NN_confidence.value)
    table_Response = get_applications_custom(con, request.offset, attributes, request.limit,
                                             json_str=True, filters=request.filter, sort=request.sort_by, sort_asc=request.sort_ascending)
    con.close()
    return table_Response


@app.get("/instance/{id}", response_model=InstanceInfo, tags=["Dataset"])
async def entire_instance_by_id(id: int):
    '''Returns the values for a loan application in the dataset, aswell as the corresponding AI recommendation and confidence provided by the `smote_ey` tensorflow model.'''
    if id > number_of_applications - 1 or id < 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={
                            "min": 0, "max": number_of_applications - 1})
    con = create_connection("database.db")
    output = get_application(con, id, json_str=True)
    con.close()
    return output


@app.post("/instance/predict", response_model=PredictionResponse, tags=["Dataset"])
async def predict_instance(instance: ModelInstanceInfo):
    """Predict the provided instance using the `smote_ey` tensorflow model. Will return `NN_recommendation` and `NN_confidence`."""

    # Checks if the provided categorical values are correctly specified, throws HTTP exception if not
    check_cat_values(instance)

    data_dict = {col: [instance.__dict__[rename_dict[col]]]
                 for col in feature_names_model_ordered}
    # Only works when all attributes are provided correctly
    df = pd.DataFrame(data_dict)
    data_to_predict = preprocessor.transform(df)
    prediction = tf_model.predict(data_to_predict)[0][0]  # list in list
    if prediction < 0.5:
        confidence = 1 - prediction
        recommendation = "Approve"
    else:
        confidence = prediction
        recommendation = "Reject"

    res = PredictionResponse(NN_confidence=confidence,
                             NN_recommendation=recommendation)
    return res


@app.get("/attributes/information", response_model=List[Union[CategoricalInformation, ContinuousInformation]], response_model_exclude_none=True, tags=["Dataset"])
async def attribute_informations():
    '''Returns a JSON with the constraints, possible values and description for each attribute.'''
    result = json.dumps(attribute_constraints)
    result = json.loads(result)
    return result


@app.post("/explanations/{exp_method}", response_model=ExplanationTaskScheduler, status_code=HTTP_202_ACCEPTED, tags=["Explanations"])
async def schedule_explanation_generation(
    instance: InstanceInfo,
    exp_method: ExplanationType,
    num_features: Optional[int] = Body(
        None, description="<b>LIME</b>: the number of features for the lime computation")
):
    '''General scheduler for **LIME** or **SHAP** explanations. **DICE** counterfactuals are already generated in the database and cannot be
    generated using this request.
    As the computations can take a large amount of time (up to 20 seconds for **SHAP**), the back-end
    returns the information that the task has been started and returns a reference (uuid) to check for & return the actual
    explantion. Notice that the front-end has to check periodically for the (status of the) result until its computation has finished.
    Only attributes specific to the explanation method (`exp_method`) will be considered.
    The back-end will use the attributes in the request body to compute an explanation. It is vital that the request
    contains each instance-attribute's respective value. (`NN_recommendation`, `NN_confidence` and `id` will be ignored if passed in the request)
    ___
    <h2>LIME</h2>

    The query parameter `num_features` is optional and if provided, will execute the <b>LIME</b> explanation with the corresponding number of features.
    ___
    '''
    # Modification
    # Add shap_orig and lime_orig as a valid explanations
    # Dice should not be used here. requests are already pregenerated in the database and can be returned directly
    if exp_method not in [ExplanationType.shap, ExplanationType.shap_orig, ExplanationType.lime, ExplanationType.lime_orig]:
        raise HTTPException(status_code=400, detail="Please use LIME or SHAP")

    check_cat_values(instance)

    job = Job(exp_type=exp_method, status=ResponseStatus.in_prog)
    job.task = {"instance": instance, "num_features": num_features}
    task_queue.put(job)

    # Modification
    # Add mapping for shap_orig
    response_mapping = {
        ExplanationType.lime:      LimeResponse,
        ExplanationType.lime_orig:      LimeResponse,
        ExplanationType.shap:      ShapResponse,
        ExplanationType.shap_orig: ShapResponse
    }

    results[job.uid] = response_mapping[exp_method](
        status=ResponseStatus.in_prog)  # Default response after subtask has started

    return ExplanationTaskScheduler(status=ResponseStatus.in_prog, href=str(job.uid))


@app.get("/explanations/lime", response_model=LimeResponse, response_model_exclude_none=True, tags=["Explanations"])
async def lime_explanation(uid: UUID):
    '''Returns the <b>LIME</b> explanation results or the status of the processing of the original request (`schedule_explanation_generation`).'''
    if uid in results.keys():
        res = results[uid]
        if type(res) != LimeResponse:
            return LimeResponse(status=ResponseStatus.wrong_method)

        return res
    else:  # In this case, there is no dict entry with this uuid
        return LimeResponse(status=ResponseStatus.not_existing)


@app.get("/explanations/lime_orig", response_model=LimeResponse, response_model_exclude_none=True, tags=["Explanations"])
async def lime_explanation(uid: UUID):
    '''Returns the <b>LIME</b> explanation results or the status of the processing of the original request (`schedule_explanation_generation`).'''
    if uid in results.keys():
        res = results[uid]
        if type(res) != LimeResponse:
            return LimeResponse(status=ResponseStatus.wrong_method)

        return res
    else:  # In this case, there is no dict entry with this uuid
        return LimeResponse(status=ResponseStatus.not_existing)


@app.get("/explanations/shap", response_model=ShapResponse, response_model_exclude_none=True, tags=["Explanations"])
async def shap_explanation(uid: UUID):
    '''Returns the <b>SHAP</b> explanation results or the status of the processing of the original request (`schedule_explanation_generation`).'''

    if uid in results.keys():
        res = results[uid]
        if type(res) != ShapResponse:
            return ShapResponse(status=ResponseStatus.wrong_method)
        return res
    else:
        return ShapResponse(status=ResponseStatus.not_existing)


@app.get("/explanations/shap_orig", response_model=ShapResponse, response_model_exclude_none=True, tags=["Explanations"])
async def shap_explanation(uid: UUID):
    '''Returns the <b>SHAP</b> explanation results or the status of the processing of the original request (`schedule_explanation_generation`).'''

    if uid in results.keys():
        res = results[uid]
        if type(res) != ShapResponse:
            return ShapResponse(status=ResponseStatus.wrong_method)
        return res
    else:
        return ShapResponse(status=ResponseStatus.not_existing)


@app.get("/explanations/dice", response_model=DiceCounterfactualResponse, response_model_exclude_none=True, tags=["Explanations"])
async def dice_explanation(instance_id: int = Query(-1, ge=0, lt=1000)):
    '''Returns the counterfactuals for the given loan application. Appends the AI prediction (`NN_recommendation`, `NN_confidence`)'''
    con = create_connection(db_path)
    cfs = get_cf(con, instance_id)
    tmp_prediction_cf = get_application(con, instance_id, True)

    for cf in cfs[counterfactuals]:
        tmp = tmp_prediction_cf.copy()  # must be the same as in databse
        for key in cf.keys():
            tmp[key] = cf[key]

        tmp_pred = {}
        for key in feature_names_model_ordered:
            tmp_pred[key] = tmp[rename_dict[key]]
        df = pd.DataFrame(tmp_pred, index=[0])

        data_to_predict = preprocessor.transform(df)
        prediction = tf_model.predict(data_to_predict)[0][0]  # list in list
        if prediction < 0.5:
            confidence = 1 - prediction
            recommendation = "Approve"
        else:
            confidence = prediction
            recommendation = "Reject"

        cf[AttributeNames.NN_confidence.value] = confidence
        cf[AttributeNames.NN_recommendation.value] = recommendation

    print(cfs)
    con.close()
    return cfs


@app.get("/processes", tags=["Debugging"])
async def process_information():
    """Returns information about the python processes that should be running."""
    return {
        "parent_process_id": os.getpid(),
        # private variable, might not be supported for different versions
        "manager_pid": manager._process.ident,
        "num_exp_processes": num_processes,
        "exp_pids": process_ids
    }


@app.get("/processes/status", tags=["Debugging"])
async def process_status(p_id: int):
    """Returns the current status of a running process based on the process id.
    Will only return information about related python processes."""
    if p_id not in [os.getpid(), manager._process.ident] + process_ids:
        return "Provided process id not related to this application."
    p = psutil.Process(p_id)
    return p.as_dict()


@app.get("/result_uids", tags=["Debugging"])
async def explanation_uids():
    """Returns the UUIDs for each explanation that is currently saved in the results dictionary."""
    return results.keys()


@app.post("/experiment/creation", status_code=HTTP_202_ACCEPTED, tags=["Experimentation"])
async def create_experiment(exp_info: ExperimentInformation):
    """Create an experiment setup and save it to the database. What-if analysis is dependent on the modification menu.
    Will yield a HTTPException if iswhatif is true but ismodify is false.
    Number of participants will get ignored if provided, will only be added once users truly complete the experiment"""
    # remove number of participants, attribute has been added on model later on and must now be caught during creation
    exp_info.num_participants = None
    # check legal boolean combination
    if len(exp_info.loan_ids) == 0:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Experiment loan applications must be specified")
    if exp_info.iswhatif:
        if exp_info.ismodify == False:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail="What-if explanation only possible if ismodify = True")
    if not set(exp_info.loan_ids).issubset(set(range(1000))):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Please specify loan-ids in the correct range.")
    exp = exp_info.json()
    con = create_connection(db_path)
    exp_creation(con, exp_info.experiment_name, exp)
    con.close()


@app.get("/experiment/all", response_model=List[str], tags=["Experimentation"])
async def experiment_list():
    """Returns a list of all experiment names, which can be used to access specific experiments."""
    con = create_connection(db_path)
    exp_list = get_all_exp(con)
    con.close()
    return exp_list


@app.get("/experiment", response_model=ExperimentInformation, tags=["Experimentation"])
async def experiment_by_name(name: str):
    """Returns the experiment setup associated to the experiment name."""
    con = create_connection(db_path)
    exp_info = get_exp_info(con, name)
    con.close()
    return exp_info


@app.post("/experiment/generate_id", response_model=ClientIDResponse, tags=["Experimentation"])
async def generate_client_id(gen: GenerateClientID):
    """Returns the next available client_id and adds that client_id to the results list. The client_id is a database reference to the
    actual user doing the experiment."""
    con = create_connection(db_path)
    return_id = create_id(con, gen.experiment_name)
    con.close()
    # check for None response! If return_id dict is None, the experiment does no exist
    if return_id is None:
        raise HTTPException(
            400, f"Experiment with name {gen.experiment_name} does not exist")
    return return_id


@app.post("/experiment/results", status_code=HTTP_202_ACCEPTED, tags=["Experimentation"])
async def results_to_database(results: ExperimentResults):
    """Adds the user-generated experiment results mapped to the client_id to the `results` table in the database."""
    con = create_connection(db_path)
    exp = get_exp_info(con, results.experiment_name)
    if not exp:  # {} is falsy and returned if experiment does not exist
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Experiment with name {results.experiment_name} not found")
    l_ids = exp["loan_ids"]
    if len(results.results) != len(l_ids):
        raise HTTPException(
            HTTP_400_BAD_REQUEST, f"Found {len(results.results)} results but should be {len(l_ids)}")
    check_loan_ids = set({})
    for res in results.results:
        check_loan_ids.add(res.loan_id)
    if set(l_ids) != check_loan_ids:
        raise HTTPException(
            HTTP_400_BAD_REQUEST, "loan_ids in results are not same as in experiment info")
    add_res(con, results.experiment_name, results.client_id, results.results)
    con.close()


@app.get("/experiment/results/export", response_model=List[ExperimentResults], tags=["Experimentation"])
async def export_results():
    """Returns all results for the chosen experiment in JSON format"""
    con = create_connection(db_path)
    result_json = export_results_to(con, ExportFormat.js_object_notation.value)
    con.close()
    return result_json


@app.get("/single/experiment/results/export", response_model=List[ExperimentResults], tags=["Experimentation"])
async def single_export_results(experiment_name: str):
    """Returns the results for the chosen experiment in json format"""
    con = create_connection(db_path)
    result_json = export_results_to(
        con, ExportFormat.js_object_notation.value, experiment_name)
    con.close()
    return result_json


@app.get("/single/experiment/results/export/csv", response_class=FileResponse, tags=["Experimentation"])
async def single_export_results_csv(experiment_name: str):
    """Returns the results for the chosen experiment in csv format. The csv file is temporarily saved on the server
    and deleted after it has been returned."""
    def cleanup():
        os.remove(temp_file)
    con = create_connection(db_path)
    temp_file = export_results_to(
        con, ExportFormat.comma_separated.value, experiment_name)
    con.close()
    return FileResponse(temp_file, background=BackgroundTask(cleanup))


@app.post("/experiment/reset", tags=["Experimentation"])
async def reset_experiment_results(experiment_name: str):
    """Deletes all results from the given experiment from the `results` table if that experiment exists."""
    con = create_connection(db_path)
    reset_exp_res(con, experiment_name)
    con.close()


@app.post("/experiment/delete", tags=["Experimentation"])
async def delete_experiment(experiment_name: str):
    """Deletes an experiment from the `experiments` table if it exists there."""
    con = create_connection(db_path)
    delete_exp(con, experiment_name)
    con.close()


@app.get("/authenticate", tags=["Security"])
async def authenticate_admin(pwd: str):
    """Is used by the frontend for simple blocking of experiment requests. THIS IS NOT A SECURE WAY TO DO SO."""
    m = hashlib.sha256()
    m.update(pwd.encode("UTF-8"))
    if m.hexdigest() != admin_pwd_hash:
        raise HTTPException(HTTP_401_UNAUTHORIZED)


# Helper methods


def check_cat_values(instance):
    # check if the categorical values are correctly specified in the request
    for key in cat_attr_check.keys():
        if instance.__dict__[key] not in cat_attr_check[key]:
            raise HTTPException(
                400, f"Please use a correct value for attribute '{key}'")


# Run main script

if __name__ == "__main__":

    # will raise NotImplementedError if count cannot be determined
    num_processes = mp.cpu_count() - 2
    manager = mp.Manager()
    results = manager.dict()
    task_queue = manager.Queue()

    print(
        f"\nMain process with id \033[96m{os.getpid()}\033[0m started succesfully. Starting {num_processes} explainer processes.\n")
    processes: List[mp.Process] = [mp.Process(target=explanation_worker, args=(
        task_queue, results)) for _ in range(num_processes)]
    for process in processes:
        process.start()
        process_ids.append(process.pid)

    uvicorn.run(app, host="0.0.0.0", port=8000)

    for process in processes:
        pid = process.pid
        process.terminate()
        print(
            f"\n\033[92mINFO:\033[0m Succesfully terminated explainer process with id \033[96m{pid}\033[0m")

    print("\n\033[92mINFO:\033[0m Application terminated.")
