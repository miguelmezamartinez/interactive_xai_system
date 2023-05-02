from enum import Enum


class ExplanationType(str, Enum):
    lime = "lime"
    lime_orig = "lime_orig"
    shap = "shap"
    shap_orig = "shap_orig"
    dice = "dice"
    none = "none"


class ExportFormat(str, Enum):
    comma_separated = "csv"
    js_object_notation = "json"


class RecommendationType(str, Enum):
    approve = "approve"
    reject = "reject"


class AttributeNames(str, Enum):
    '''This class is used to have a central definition of how the attributes are referenced'''
    # attributes in the dataset
    balance = "balance"
    duration = "duration"
    history = "history"
    purpose = "purpose"
    amount = "amount"
    savings = "savings"
    employment = "employment"
    available_income = "available_income"
    #status_sex = "status_sex"
    residence = "residence"
    assets = "assets"
    age = "age"
    other_loans = "other_loans"
    housing = "housing"
    previous_loans = "previous_loans"
    job = "job"
    telephone = "telephone"
    #foreign_worker = "foreign_worker"
    other_debtors = "other_debtors"
    people_liable = "people_liable"

    # meta-attributes
    ident = "id"
    NN_recommendation = "NN_recommendation"
    NN_confidence = "NN_confidence"


class ResponseStatus(str, Enum):
    in_prog = "in progress"
    terminated = "terminated"
    timeout = "timeout"
    error = "error"
    not_existing = "No explanation result with corresponding uuid"
    wrong_method = "Uuid corresponds to antoher explanation method"


# standard configuration for table view
standard_attributes = [
    AttributeNames.amount,
    AttributeNames.duration,
    AttributeNames.balance,
    AttributeNames.age,
    AttributeNames.employment
]

# number definitions to re-use through the entire code
row_limit = 20

# strings to use throughout the entire code (important for coherence in response-key names)
original_instance = "original_instance"
attr_name = "attribute"
attr_name_abr = "attr_name"
const_type = "type"
values = "values"
categorical = "categorical"
continuous = "continuous"
lower_bound = "lower_bound"
upper_bound = "upper_bound"
attr_description = "description"
influence = "influence"
#pred_proba = "pred_proba"
#recommendation = "recommendation"
positive_influence = "positive_influence"
category = "category"
financial_cat = "financial"
personal_cat = "personal"
loan_cat = "loan"
prediction_cat = "prediction"
filter = "filter"
attributes = "attributes"
sort_by = "sort_by"
limit = "limit"
offset = "offset"
num_features = "num_features"
base_value = "base_value"
counterfactuals = "counterfactuals"
status = "status"
process_id = "process_id"
href = "href"
lime_result = "lime_result"
display_name = "display_name"
sort_ascending = "sort_ascending"
counterfactuals = "counterfactuals"
const_type = "type"
values = "values"
db_path = "database.db"
csv_path = "results.csv"
results_key = "results"
loan_id = "loan_id"
client_id = "client_id"
timestamp = "timestamp"
choice = "choice"
all_features = 18
number_of_applications = 1000
timeout_seconds = 180
timestamp = "timestamp"

# attribute constraints must exactly conform to the possible values accepted by the model!
attribute_constraints = [
    {
        attr_name: AttributeNames.balance,
        const_type: categorical,
        category: financial_cat,
        # List[str]
        values: ['no account', 'no balance', 'below 200 EUR', 'above 200 EUR'],
        attr_description: "The current balance of the applicant's checking account (in Euros)"
    },
    {
        attr_name: AttributeNames.duration,
        const_type: continuous,
        category: loan_cat,
        lower_bound: 4,  # float
        upper_bound: 72,  # float
        attr_description: "The duration of the loan (in months)"
    },
    {
        attr_name: AttributeNames.history,
        const_type: categorical,
        category: financial_cat,
        values: ['delay payment of previous loans', 'paid back previous loans at this bank', 'paid back all previous loans', 'no problems with current loans', 'other loans exist at other banks'],
        attr_description: "How reliably the applicant handled previous or current loans"
    },
    {
        attr_name: AttributeNames.purpose,
        const_type: categorical,
        category: loan_cat,
        values: ['furniture', 'television', 'used car', 'domestic appliances', 'repair', 'retraining', 'business', 'new car', 'other', 'vacation'],
        attr_description: "The purpose for which the loan money will be used for"
    },
    {
        attr_name: AttributeNames.amount,
        const_type: continuous,
        category: loan_cat,
        lower_bound: 250,
        upper_bound: 11792.5,
        attr_description: "How much money the applicant wants to borrow (in Euro)"
    },
    {
        attr_name: AttributeNames.savings,
        const_type: categorical,
        category: financial_cat,
        values: ['no savings account at this bank', 'below 100 EUR', 'between 100 and 500 EUR', 'between 500 and 1000 EUR', 'above 1000 EUR'],
        attr_description: "Amount of savings at that bank (in Euros)"
    },
    {
        attr_name: AttributeNames.employment,
        const_type: categorical,
        category: personal_cat,
        values: ['unemployed', 'less than 1 year', 'between 1 and 4 years', 'between 4  and 7 years', 'more than 7 years'],
        attr_description: "How long has the applicant been working in current employment"
    },
    {
        attr_name: AttributeNames.available_income,
        const_type: categorical,
        category: financial_cat,
        values: ['less than 20%', 'between 20 and 25%', 'between 25 and 35%', 'more than 35%'],
        attr_description: "Percentage of income available after fixed costs that the applicant could use for repaying the loan"
    },
    {
        attr_name: AttributeNames.residence,
        const_type: categorical,
        category: personal_cat,
        values: ['less than 1 year', 'between 1 and 4 years', 'between 4 and 7 years', 'more than 7 years'],
        attr_description: "How long has the applicant lived in the current housing"
    },
    {
        attr_name: AttributeNames.assets,
        const_type: categorical,
        category: financial_cat,
        values: ['none', 'life insurance', 'car', 'real estate'],
        attr_description: "Applicant's most valuable available asset to be used as a collateral payment"
    },
    {
        attr_name: AttributeNames.age,
        const_type: continuous,
        category: personal_cat,
        lower_bound: 19,
        upper_bound: 75,
        attr_description: "The age of the loan applicant"
    },
    {
        attr_name: AttributeNames.other_loans,
        const_type: categorical,
        category: financial_cat,
        values: ['no additional loans', 'at department store', 'at other banks'],
        attr_description: "Applicant's additional loans"
    },
    {
        attr_name: AttributeNames.housing,
        const_type: categorical,
        category: personal_cat,
        values: ['rent', 'for free', 'own'],
        attr_description: "Whether the applicant pays rent for housing, owns or lives for free"
    },
    {
        attr_name: AttributeNames.previous_loans,
        const_type: categorical,
        category: financial_cat,
        values: ['1', '2 or 3', '4 or more'],
        attr_description: "Number of loans the applicant has already had"
    },
    {
        attr_name: AttributeNames.job,
        const_type: categorical,
        category: personal_cat,
        values: ['unskilled (non-resident)', 'unskilled (permanent resident)', 'skilled', 'executive or self-employed'],
        attr_description: "Type of profession"
    },
    {
        attr_name: AttributeNames.other_debtors,
        const_type: categorical,
        category: loan_cat,
        values: ['none', 'co-applicant', 'guarantor'],
        attr_description: "Whether there are additional people that act as a guarantee for the loan"
    },
    {
        attr_name: AttributeNames.people_liable,
        const_type: categorical,
        category: personal_cat,
        values: ['0 to 2', '3 and more'],
        attr_description: "Number of people that depend financially on the applicant"
    },
    {
        attr_name: AttributeNames.NN_confidence,
        const_type: continuous,
        category: prediction_cat,
        lower_bound: 0.5,
        upper_bound: 1,
        attr_description: "Indicates how confident the AI is in it's decision."
    },
    {
        attr_name: AttributeNames.NN_recommendation,
        const_type: categorical,
        category: prediction_cat,
        values: ['Reject', 'Approve'],
        attr_description: "The AI's recommendation whether the loan application should be approved or rejected"
    },
    {
        attr_name: AttributeNames.telephone,
        const_type: categorical,
        category: personal_cat,
        values: ['none', 'yes'],
        attr_description: "Whether telephone information is provided"
    }
]

# Dictionary generated from attribute constraints to check values passed to API
cat_attr_check = {constr[attr_name].value: constr[values]
                  for constr in attribute_constraints if "NN" not in constr[attr_name] and constr[const_type] is categorical}

rename_dict = {
    'balance_': AttributeNames.balance.value,
    'duration_': AttributeNames.duration.value,
    'history_': AttributeNames.history.value,
    'purpose_': AttributeNames.purpose.value,
    'amount_': AttributeNames.amount.value,
    'savings_': AttributeNames.savings.value,
    'employment_': AttributeNames.employment.value,
    'available_income_': AttributeNames.available_income.value,
    'other_debtors_': AttributeNames.other_debtors.value,
    'residence_': AttributeNames.residence.value,
    'assets_': AttributeNames.assets.value,
    'age_': AttributeNames.age.value,
    'other_loans_': AttributeNames.other_loans.value,
    'housing_': AttributeNames.housing.value,
    'previous_loans_': AttributeNames.previous_loans.value,
    'job_': AttributeNames.job.value,
    'people_liable_': AttributeNames.people_liable.value,
    'telephone_': AttributeNames.telephone.value
}

inv_rename = {v: k for k, v in rename_dict.items()}

# MUST STAY IN THIS ORDER!
feature_names_model_ordered = [
    'balance_',
    'duration_',
    'history_',
    'purpose_',
    'amount_',
    'savings_',
    'employment_',
    'available_income_',
    'other_debtors_',
    'residence_',
    'assets_',
    'age_',
    'other_loans_',
    'housing_',
    'previous_loans_',
    'job_',
    'people_liable_',
    'telephone_'
]

lime_exp_mapping = {
    0: AttributeNames.balance.value,
    1: AttributeNames.duration.value,
    2: AttributeNames.history.value,
    3: AttributeNames.purpose.value,
    4: AttributeNames.amount.value,
    5: AttributeNames.savings.value,
    6: AttributeNames.employment.value,
    7: AttributeNames.available_income.value,
    8: AttributeNames.other_debtors.value,
    9: AttributeNames.residence.value,
    10: AttributeNames.assets.value,
    11: AttributeNames.age.value,
    12: AttributeNames.other_loans.value,
    13: AttributeNames.housing.value,
    14: AttributeNames.previous_loans.value,
    15: AttributeNames.job.value,
    16: AttributeNames.people_liable.value,
    17: AttributeNames.telephone.value
}
