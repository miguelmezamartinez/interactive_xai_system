# To run these tests, cd to the API folder, run the main app
# and once the API has finished startup, run pytest -s in another terminal session

# imports

import pytest
import requests
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_404_NOT_FOUND,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
)
import time
import numpy as np
from tqdm import tqdm
import threading

# Helper methods

api_path = "http://localhost:8000/"


def route(path: str):
    """Will return the appended root path with the input string"""
    return api_path + path


def r_get(path: str):
    """Will return the requests response object.

    :param: path: The request's path relative to the server root."""
    return requests.get(route(path))


def r_post(path: str, json):
    """Will return the requests response object for a post request.

    :param: path: The request's path relative to the server root.
    :param: json: The data (request body) that should be passed to the post request"""
    return requests.post(route(path), json=json)


# Test methods

def test_empty_results():
    assert len(r_get("result_uids").json()) == 0

def test_get_instance_by_id():
    res = r_get("instance/0").json()
    assert res["id"] == 0
    assert len(res.keys()) == 21
    res = r_get("instance/-12")
    assert res.status_code == HTTP_404_NOT_FOUND
    res = r_get("instance/1000")
    assert res.status_code == HTTP_404_NOT_FOUND
    res = r_get("instance/124asghla")  # gibberish query
    assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_table_bad_request():
    request_data = {
        "filter": [
            {
                "attribute": "balance",
                "lower_bound": 2000,
                "upper_bound": 5000,
            }  # should be categorical
        ],
        "attributes": ["amount"],
        "limit": 10,
        "offset": 0,
    }

    res = r_post("table", request_data)
    assert len(res.json()) == 0

    # checking if pydantic data validation works for filter "assets"
    request_data = {
        "filter": [
            {"attribute": "assets", "lower_bound": ["car", "real estate"]},
            {"attribute": "housing", "values": ["for free", "own"]},
            {
                "attribute": "employment",
                "values": ["unemployed", "between 1 and 4 years", "more than 7 years"],
            },
            {"attribute": "amount", "lower_bound": 1140, "upper_bound": 8612},
        ],
        "attributes": ["balance", "duration", "amount", "age", "savings"],
        "sort_by": "id",
        "sort_ascending": True,
        "desc": False,
        "limit": 100,
        "offset": 0,
    }
    res = r_post("table", request_data)
    assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_table_false_values():
    # false values for balance
    request_data = {
        "filter": [
            {"attribute": "assets", "values": ["car", "real estate"]},
            {"attribute": "housing", "values": ["for free", "own"]},
            {
                "attribute": "employment",
                "values": ["unemployed", "between 1 and 4 years", "more than 7 years"],
            },
            {"attribute": "amount", "lower_bound": 1140, "upper_bound": 8612},
        ],
        "attributes": ["balance", "duration", "amount", "age", "savings"],
        "sort_by": "id",
        "sort_ascending": True,
        "desc": False,
        "limit": 100,
        "offset": 0,
    }
    res = r_post("table", request_data)
    assert res.status_code == 200


def test_time_table():
    request_data = {
        "filter": [
            {"attribute": "assets", "values": ["car", "real estate"]},
            {"attribute": "housing", "values": ["for free", "own"]},
            {
                "attribute": "employment",
                "values": ["unemployed", "between 1 and 4 years", "more than 7 years"],
            },
            {"attribute": "amount", "lower_bound": 1140, "upper_bound": 8612},
        ],
        "attributes": ["balance", "duration", "amount", "age", "savings"],
        "sort_by": "id",
        "sort_ascending": True,
        "desc": False,
        "limit": 100,
        "offset": 0,
    }
    times = []
    from tqdm import tqdm

    for _ in tqdm(range(1000)):
        start = time.time_ns()
        res = r_post("table", request_data)
        end = time.time_ns()
        times.append((end - start) / 1e6)
    print("Average table request duration in ms: ", np.mean(times))
    assert np.mean(times) < 50  # assert less than 50 milliseconds per request on average
    assert len(res.json()) > 0


def test_exp_generation_lime():
    request_data = {
            "instance": {
                "id" : -1,
                "balance": "above 200 EUR",
                "duration": 12,
                "history": "paid back previous loans at this bank",
                "purpose": "repair",
                "amount": 2096,
                "savings": "no savings account at this bank",
                "employment": "between 4  and 7 years",
                "available_income": "between 25 and 35%",
                "residence": "between 4 and 7 years",
                "assets": "real estate",
                "age": 49,
                "other_loans": "no additional loans",
                "housing": "own",
                "previous_loans": "1",
                "job": "unskilled (permanent resident)",
                "other_debtors": "none",
                "people_liable": "3 and more",
                "telephone": "none"
            },
            "num_features": 18
        }

    res = r_post("explanations/lime", request_data)
    assert res.status_code == HTTP_202_ACCEPTED
    assert res.json()["status"] == "in progress"
    uid = res.json()["href"]

    while res.json()["status"] == "in progress":
        res = r_get(f"explanations/lime?uid={uid}")
        if res.json()["status"] == "terminated":
            assert len(res.json()["values"]) == 18

def test_multiple_lime():
    uids = []
    num_trials = 20
    request_data = {
            "instance": {
                "id" : -1,
                "balance": "above 200 EUR",
                "duration": 12,
                "history": "paid back previous loans at this bank",
                "purpose": "repair",
                "amount": 2096,
                "savings": "no savings account at this bank",
                "employment": "between 4  and 7 years",
                "available_income": "between 25 and 35%",
                "residence": "between 4 and 7 years",
                "assets": "real estate",
                "age": 49,
                "other_loans": "no additional loans",
                "housing": "own",
                "previous_loans": "1",
                "job": "unskilled (permanent resident)",
                "other_debtors": "none",
                "people_liable": "3 and more",
                "telephone": "none"
            },
            "num_features": 18
        }

    for _ in range(num_trials):
        res = r_post("explanations/lime", request_data)
        uids.append(res.json()["href"])

    def thread_worker(uid):
        res = r_get(f"explanations/lime?uid={uid}").json()
        while res["status"] != "terminated":
            res = r_get(f"explanations/lime?uid={uid}").json()
        
        assert len(res["values"]) == 18
    
    threads = []

    for i in range(num_trials):
        t = threading.Thread(target=thread_worker, args=(uids[i],))
        t.start()
        threads.append(t)

    print("Testing multiple lime requests:")
    for i in tqdm(range(num_trials)):
        threads[i].join()

    # Making sure the results are all saved in the dictionary
    assert len(r_get("result_uids").json()) == num_trials + 1

@pytest.mark.skip(reason="Takes too long.")
def test_multiple_shap():
    uids = []
    num_trials = 10
    request_data = {
            "instance": {
                "id" : -1,
                "balance": "above 200 EUR",
                "duration": 12,
                "history": "paid back previous loans at this bank",
                "purpose": "repair",
                "amount": 2096,
                "savings": "no savings account at this bank",
                "employment": "between 4  and 7 years",
                "available_income": "between 25 and 35%",
                "residence": "between 4 and 7 years",
                "assets": "real estate",
                "age": 49,
                "other_loans": "no additional loans",
                "housing": "own",
                "previous_loans": "1",
                "job": "unskilled (permanent resident)",
                "other_debtors": "none",
                "people_liable": "3 and more",
                "telephone": "none"
            }
        }

    for _ in range(num_trials):
        res = r_post("explanations/shap", request_data)
        uids.append(res.json()["href"])

    def thread_worker(uid):
        res = r_get(f"explanations/shap?uid={uid}").json()
        while res["status"] != "terminated":
            res = r_get(f"explanations/shap?uid={uid}").json()
        
        assert len(res["values"]) == 18
        assert "base_value" in res.keys()
    
    threads = []

    for i in range(num_trials):
        t = threading.Thread(target=thread_worker, args=(uids[i],))
        t.start()
        threads.append(t)

    print(f"Testing multiple ({num_trials}) shap requests:")
    for i in tqdm(range(num_trials)):
        threads[i].join()

def test_explanation_processes_running():
    print("Checking if explanation processes are still alive:")
    process_ids = r_get("processes").json()["exp_pids"]
    for pid in tqdm(process_ids):
        assert r_get(f"processes/status?p_id={pid}").json()["status"] == "running"

# Testing for experimental mode

def test_good_exp_creation():
    data = {
        "loan_ids" : [0, 12, 100],
        "ismodify" : True,
        "iswhatif" : False,
        "exp_type" : "lime",
        "experiment_name" : "Pytesting Experiments",
        "description" : "This is an experiment with a description"
    }

    r = r_post("experiment/creation", data)
    assert r.status_code == HTTP_202_ACCEPTED

def test_outofbounds_exp_creation():
    data = {
        "loan_ids" : [80, -12, 900, 1200],
        "ismodify" : True,
        "iswhatif" : False,
        "exp_type" : "lime",
        "experiment_name" : "Secondtest",
        "description" : "any description"
    }

    r = r_post("experiment/creation", data)
    assert r.status_code == HTTP_400_BAD_REQUEST
    assert r.json()["detail"] == "Please specify loan-ids in the correct range."

def test_wrongcombination_exp_creation():
    data = {
        "loan_ids" : [100, 12],
        "ismodify" : False,
        "iswhatif" : True,
        "exp_type" : "lime",
        "experiment_name" : "Secondtest",
        "description" : "any description"
    }

    r = r_post("experiment/creation", data)
    assert r.status_code == HTTP_400_BAD_REQUEST
    assert r.json()["detail"] == "What-if explanation only possible if ismodify = True"

def test_empytlist_exp_creation():
    data = {
        "loan_ids" : [],
        "ismodify" : False,
        "iswhatif" : False,
        "exp_type" : "shap",
        "experiment_name" : "Thirdtest",
        "description" : "any description"
    }

    r = r_post("experiment/creation", data)
    assert r.status_code == HTTP_400_BAD_REQUEST
    assert r.json()["detail"] == "Experiment loan applications must be specified"

def test_get_experiment():
    r = r_get("experiment?name=Pytesting Experiments")
    assert r.status_code == 200

def test_experiment_id():
    for _ in range(20):
        r = r_post("experiment/generate_id", {"experiment_name" : "Pytesting Experiments"})
    assert r.json()["client_id"] == 19

def test_generate_results():
    data = {
        "experiment_name" : "Pytesting Experiments",
        "client_id" : 0,
        "results" : [
            {"loan_id" : 0, "choice" : "approve"},
            {"loan_id" : 12, "choice" : "approve"},
            {"loan_id" : 100, "choice" : "approve"}
        ] 
    }
    r = r_post("experiment/results", data)
    assert r.status_code == HTTP_202_ACCEPTED

def test_falseid_generate_results():
    # False loan_id
    data = {
        "experiment_name" : "Pytesting Experiments",
        "client_id" : 1,
        "results" : [
            {"loan_id" : 69, "choice" : "approve"},
            {"loan_id" : 120, "choice" : "approve"},
            {"loan_id" : 100, "choice" : "approve"}
        ] 
    }
    r = r_post("experiment/results", data)
    assert r.status_code == HTTP_400_BAD_REQUEST

def test_falselength_generate_results():
    data = {
        "experiment_name" : "Pytesting Experiments",
        "client_id" : 1,
        "results" : [
            {"loan_id" : 1, "choice" : "approve"},
            {"loan_id" : 12, "choice" : "approve"},
            {"loan_id" : 100, "choice" : "approve"},
            {"loan_id" : 100, "choice" : "approve"}
        ] 
    }
    r = r_post("experiment/results", data)
    assert r.status_code == HTTP_400_BAD_REQUEST
    assert "results but should be" in r.json()["detail"]

def test_falsename_generate_results():
    data = {
        "experiment_name" : "THISNAMEISWRONG",
        "client_id" : 0,
        "results" : [
            {"loan_id" : 0, "choice" : "approve"},
            {"loan_id" : 12, "choice" : "approve"},
            {"loan_id" : 100, "choice" : "approve"}
        ] 
    }
    r = r_post("experiment/results", data)
    assert r.status_code == HTTP_404_NOT_FOUND

# TODO test deletion of experiment

# TODO test reset of experiment