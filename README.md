# Development of an Interactive Explainable AI System for End-users

---

**Paper**: Designing Interactive Explainable AI Systems for End-users

**Authors**: Miguel Angel Meza Martínez & Alexander Maedche

**Developers**: Felix Hasse, Nicolas Kiefer, Isabelle Konrad, Tilio Schulze & Miguel Angel Meza Martínez

**Version**: 1.0

[[_TOC_]]

## First Steps

### Environment and dependencies

#### Frontend

1. Make sure that the version 16 of [Node.js](https://nodejs.org/en/) is installed on your system
2. Run the following commands in a terminal in the project base directory

```shell
npm install -g @vue/cli
npm install -g @vue/cli-service
cd Frontend/app
npm install
```

#### Backend

The python requirements are saved in the API folder. Depending on your os, choose the requirements file and create an environment with either conda or install directly with pip.
Additionally, make sure to initialize the database running the following script

```shell
cd API/scr/
python database_creation.py
```

### Run application

Terminal 1:

```shell
cd API/scr/
python main.py
```

Terminal 2:

```shell
cd Frontend/app/
npm run serve
```

Interactive API docs are accessible with http://localhost:8000/docs.
The root for all API requests is http://localhost:8000/. \
The application GUI is accessible with http://localhost:8080/.
The starting page is "/dataset". To access the admin panel, use "/admin".

## Project structure

The application consists of a web-based frontend GUI and a backend API server. The frontend is built with the [Vue.js](https://vuejs.org) framework, the API with the [FastAPI](https://fastapi.tiangolo.com)-Python framework.

![project structure](/uploads/structure.png)

## Backend

### Overview of Files

The Backend files can be found in the folder "API/". Here is a short summary about what each file or directory does:

`main.py`:

- starting point for FastAPI process
- defines the API requests accessible by the front-end
- contains documentation for interactive FastAPI docs (http://localhost:8000/docs)
- launches explanation sub-processes defined in `task_gen.py`
- defines manager process for shared process memory

`models.py`:

- defines the [pydantic](https://pydantic-docs.helpmanual.io) models for requests, responses and other data schemas
- using models ensures data validation and basic type conversion

`constants.py`:

- defines commonly used strings and numbers to reduce magic strings
- contains the constraints for the dataset attributes
- defines dictionary mappings for data transformations

`database_req.py`:

- interface for database interaction with the API
- defines functions for database access, seperates database logic and structure from API requests

`task_gen.py`:

- defines explanation sub-process logic for lime and shap
- access to shared memory (job queue, explanation results dictionary)
- defines timeout logic for explanation results

`lime_utils.py`:

- Helper class for the [lime](https://github.com/marcotcr/lime) explanation generation
- uses code from the xai reference project
- loads the german credit dataset and the `smote_ey.tf` model and fits a preprocessor
- creates a lime explanainer
- contains method to get lime explanation for a given instance and return it in the json format specified by the API

`shap_utils.py`:

`preproc.pickle`:

`DataLoader_ey.py`:

- taken from the xai reference project and slightly adapted
- method data_loader to load the credit data, drop the unused columns and remove outliers
- preprocessing method for preparing data for model prediction
- method for adding AI recommendation and confidence

`database.db`:

- SQLite database for application, counterfactual information and experimentation information storage
- overview over structure and methods provided below

`smote_ey.tf/`:

- the trained tensorflow model from the xai reference project
- used for AI recommendation and confidence and explanation generation

`Data/`:

- folder containing the raw data that was read into the database
- contains the german credit dataset in csv format and
- contains the counterfactuals in json format, the `all_counterfactuals.json` contains the initially generated counterfactuals, the `cfs_response_format.json` a reformatted version of the counterfactuals that was added to the database

### SQLite Database

The application uses a SQLite database for saving the cleaned german credit dataset ([GCD](https://archive.ics.uci.edu/ml/datasets/Statlog+%28German+Credit+Data%29)), the experiments and the corresponding results, aswell as pre-generated `DICE` counterfactuals for each loan application. The python module [SQLite3](https://docs.python.org/3.8/library/sqlite3.html) is used as the database interface for the API.
\
An overview of the different tables and their strucutre is provided below. Below that, you can find an overview of the relevant database interaction functions. These are defined in the file `database_req.py` which is located in the "API/" folder

---

**Database Table Structure:**
![Database Table Structure](/uploads/database_structure.png)
All cleaned applications from the GCD are stored in the applicants table. The attributes foreign*worker, status_sex* and classification\_ were dropped and NN_recommendation and NN_confidence added. These two attributes refer to the actual model prediction for this application and were determined using the `smote_ey.tf` model.\
The dice table contains the pregenerated counterfactuals for the applications of the GCD. The counterfactuals column contains this information in json format. These jsons have the key 'counterfactuals' referring to a list of 5 counterfactuals in json format. This is necessary because SQLite cannot store lists.\
The elements in the dice table have the primary key instance_id, which refers to the ids in the applicants table. Therefore when an element in the applicants table is deleted or changes its id, the according element in the dice table should be deleted or changed as well.\
The experimentation functionality is covered by the databases experiments and results. In the experiments table all the relevant information for the defined experiments, like the type of explanation and ids of applications that should be shown are stored in json format. The json contains the keys, which are defined for the ExperimentInformation model in the `models.py` file. The results table is used to store the decisions of a user for a certain experiment. They are stored in json format. The json contains jsons in the SingleResult format defined in the `models.py` folder. Their loan id is the key to reference those SingleResult jsons.\
The key experiment_name of the results table references the attribute name in the experiments table. Therefore when an experiment is deleted or changes its name, this change should also apply to the results table.

---

**Database Interaction:**
![Database Interaction](/uploads/database_interaction.png)

---

### XAI Explanations

The XAI methods used in this project are `LIME`, `SHAP` and `DICE`. As the generation of counterfactuals using `DICE` takes a large amount of time (1,5 - 3 minutes), the counterfactuals have been pre-generated for each instance of the GCD dataset and stored in the data table. They can thus not be dynamically generated. \
For `SHAP` and `LIME` however, the explanations are computed in the backend, which makes it possible to dynamically generate what-if analysis for modified dataset instances.\
To efficiently generate explanations, the API scans the number of available CPU cores of the server it is running on, and generated calculation processes accordingly. The sole task of these calculation processes is to generate explanations when clients request them.\
The requested explanation tasks are saved in a FIFO-queue to which all calculation processes have access. One of the running calculation processes will take the task from the queue and will return it in a process-shared dictionary when it has finished generating the explanation. The user can access the generated explanation using the id returned by the API when the explanation was scheduled.

Explanation Task flow: `rgb(133, 192, 255)`\
Explanation Result flow: `rgb(217, 155, 255)`
![Explanations compuation & data flow](/uploads/api_explainer.jpg)

## Front-End

You can find detailed documentation of all components used in the Frontend [here](Frontend/app/docs)
