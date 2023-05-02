from fastapi.params import Body
from pydantic import BaseModel, Field
from typing import Optional, List, Union

from constants import *


class InstanceInfo(BaseModel):
    '''Defines how a JSON model for an instance information should look like.
    Maps the predefined names for attributes as the alias of the pydantic class keys.'''

    ident: int = Field(alias=AttributeNames.ident.value, ge=-1, le=1000)
    balance: Optional[str] = Field(None, alias=AttributeNames.balance.value)
    duration: Optional[float] = Field(
        None, alias=AttributeNames.duration.value)
    history: Optional[str] = Field(None, alias=AttributeNames.history.value)
    purpose: Optional[str] = Field(None, alias=AttributeNames.purpose.value)
    amount: Optional[float] = Field(None, alias=AttributeNames.amount.value)
    savings: Optional[str] = Field(None, alias=AttributeNames.savings.value)
    employment: Optional[str] = Field(
        None, alias=AttributeNames.employment.value)
    available_income: Optional[str] = Field(
        None, alias=AttributeNames.available_income.value)
    residence: Optional[str] = Field(
        None, alias=AttributeNames.residence.value)
    assets: Optional[str] = Field(None, alias=AttributeNames.assets.value)
    age: Optional[float] = Field(None, alias=AttributeNames.age.value)
    other_loans: Optional[str] = Field(
        None, alias=AttributeNames.other_loans.value)
    housing: Optional[str] = Field(None, alias=AttributeNames.housing.value)
    previous_loans: Optional[str] = Field(
        None, alias=AttributeNames.previous_loans.value)
    job: Optional[str] = Field(None, alias=AttributeNames.job.value)
    other_debtors: Optional[str] = Field(
        None, alias=AttributeNames.other_debtors.value)
    people_liable: Optional[str] = Field(
        None, alias=AttributeNames.people_liable.value)
    telephone: Optional[str] = Field(
        None, alias=AttributeNames.telephone.value)
    NN_recommendation: Optional[str] = Field(
        None, alias=AttributeNames.NN_recommendation.value)
    NN_confidence: Optional[float] = Field(
        None, le=1, ge=0, alias=AttributeNames.NN_confidence.value)

    class Config:
        orm_mode = True


class ModelInstanceInfo(BaseModel):
    '''Defines the JSON loan application model for all requests that need the tensorflow model to make a prediction.
    All 18 features <b>must</b> be included.'''

    balance: str = Field(alias=AttributeNames.balance.value)
    duration: float = Field(alias=AttributeNames.duration.value)
    history: str = Field(alias=AttributeNames.history.value)
    purpose: str = Field(alias=AttributeNames.purpose.value)
    amount: float = Field(alias=AttributeNames.amount.value)
    savings: str = Field(alias=AttributeNames.savings.value)
    employment: str = Field(alias=AttributeNames.employment.value)
    available_income: str = Field(alias=AttributeNames.available_income.value)
    residence: str = Field(alias=AttributeNames.residence.value)
    assets: str = Field(alias=AttributeNames.assets.value)
    age: float = Field(alias=AttributeNames.age.value)
    other_loans: str = Field(alias=AttributeNames.other_loans.value)
    housing: str = Field(alias=AttributeNames.housing.value)
    previous_loans: str = Field(alias=AttributeNames.previous_loans.value)
    job: str = Field(alias=AttributeNames.job.value)
    other_debtors: str = Field(alias=AttributeNames.other_debtors.value)
    people_liable: str = Field(alias=AttributeNames.people_liable.value)
    telephone: str = Field(alias=AttributeNames.telephone.value)


class CounterFactual(BaseModel):
    """Defines the JSON model for a counterfactual, where only attributes are set,
    that have changed in relation to the original instance"""
    balance: Optional[str] = Field(None, alias=AttributeNames.balance.value)
    duration: Optional[float] = Field(
        None, alias=AttributeNames.duration.value)
    history: Optional[str] = Field(None, alias=AttributeNames.history.value)
    purpose: Optional[str] = Field(None, alias=AttributeNames.purpose.value)
    amount: Optional[float] = Field(None, alias=AttributeNames.amount.value)
    savings: Optional[str] = Field(None, alias=AttributeNames.savings.value)
    employment: Optional[str] = Field(
        None, alias=AttributeNames.employment.value)
    available_income: Optional[str] = Field(
        None, alias=AttributeNames.available_income.value)
    residence: Optional[str] = Field(
        None, alias=AttributeNames.residence.value)
    assets: Optional[str] = Field(None, alias=AttributeNames.assets.value)
    age: Optional[float] = Field(None, alias=AttributeNames.age.value)
    other_loans: Optional[str] = Field(
        None, alias=AttributeNames.other_loans.value)
    housing: Optional[str] = Field(None, alias=AttributeNames.housing.value)
    previous_loans: Optional[str] = Field(
        None, alias=AttributeNames.previous_loans.value)
    job: Optional[str] = Field(None, alias=AttributeNames.job.value)
    other_debtors: Optional[str] = Field(
        None, alias=AttributeNames.other_debtors.value)
    people_liable: Optional[str] = Field(
        None, alias=AttributeNames.people_liable.value)
    telephone: Optional[str] = Field(
        None, alias=AttributeNames.telephone.value)
    NN_recommendation: str = Field(
        alias=AttributeNames.NN_recommendation.value)
    NN_confidence: float = Field(alias=AttributeNames.NN_confidence.value)


class PredictionResponse(BaseModel):
    '''Defines the response format for a prediction call.'''
    NN_recommendation: str = Field(
        alias=AttributeNames.NN_recommendation.value)
    NN_confidence: float = Field(alias=AttributeNames.NN_confidence.value)


class ContinuousFilter(BaseModel):
    '''Defines the JSON format for a continuous filter request body'''
    attr_name: AttributeNames = Field(alias=attr_name)
    lower_bound: float = Field(alias=lower_bound)
    upper_bound: float = Field(alias=upper_bound)


class CategoricalFilter(BaseModel):
    '''Defines the JSON format for a categorical filter request body'''
    attr_name: AttributeNames = Field(alias=attr_name)
    values: List[str] = Field(alias=values)


class TableRequest(BaseModel):
    filter: Optional[List[Union[ContinuousFilter, CategoricalFilter]]] = Field(
        None, alias=filter)
    attributes: List[AttributeNames] = Field(
        standard_attributes, alias=attributes)
    sort_by: AttributeNames = Field(AttributeNames.ident, alias=sort_by)
    sort_ascending: bool = Field(True, alias=sort_ascending)
    limit: int = Field(row_limit, alias=limit)
    offset: int = Field(0, alias=offset)


class CategoricalInformation(BaseModel):
    '''Defines the JSON format for the constraints of a categorical attribute'''
    attr_name: AttributeNames = Field(alias=attr_name)
    display_name: Optional[str] = Field(None, alias=display_name)
    type: str = Field(categorical, const=True, alias=const_type)
    category: str = Field(alias=category)
    values: List[str]
    description: str = Field(alias=attr_description)


class ContinuousInformation(BaseModel):
    '''Defines the JSON format for the constraints of a categorical attribute'''
    attr_name: AttributeNames = Field(alias=attr_name)
    display_name: Optional[str] = Field(None, alias=display_name)
    type: str = Field(continuous, const=True, alias=const_type)
    category: str = Field(alias=category)
    lower_bound: float = Field(alias=lower_bound)
    upper_bound: float = Field(alias=upper_bound)
    description: str = Field(alias=attr_description)


class ExplanationTaskScheduler(BaseModel):
    '''This class gives a response to monitor the status of the explanations which might take a long time in computation.
    with the href and the process_id, the front-end can send requests to the api to get the explanation object back.'''
    status: ResponseStatus = Field(alias=status)
    process_id: Optional[int] = Field(None, alias=process_id)
    href: str = Field(alias=href)


class LimeResponse(BaseModel):
    '''JSON format for `LIME` model response.
    The actual results are only returned if the process is terminated.'''
    class LimeAttribute(BaseModel):
        attr_name: AttributeNames = Field(alias=attr_name)
        influence: float = Field(alias=influence)
    status: ResponseStatus = Field(alias=status)
    # Modification
    # Adding base value for LIME
    base_value: Optional[float] = Field(
        None, alias=base_value, description="The model's expected prediciton outcome which is used in the plot.\n`None`, when process has not terminated.")
    values: Optional[List[LimeAttribute]] = Field(
        None, alias=values, description="The <b>LIME</b> results.\n`None`, when process has not terminated.")


class ShapResponse(BaseModel):
    '''JSON format for `SHAP` model response. The actual results are only returned if the process is terminated.'''
    class ShapAttribute(BaseModel):
        '''Defines the JSON format for an element of the <b>SHAP</b> explanation'''
        attr_name: AttributeNames = Field(alias=attr_name)
        influence: float = Field(alias=influence)
    status: ResponseStatus = Field(alias=status)
    base_value: Optional[float] = Field(
        None, alias=base_value, description="The model's expected prediciton outcome which is used in the plot.\n`None`, when process has not terminated.")
    values: Optional[List[ShapAttribute]] = Field(
        None, alias=values, description="The <b>SHAP</b> results.\n`None`, when process has not terminated.")
    # Modification Backup
    # Adding prediction probability
    #pred_proba: Optional[float] = Field(alias=pred_proba)
    #recommendation: Optional[str] = Field(alias=recommendation)


class DiceCounterfactualResponse(BaseModel):
    '''JSON format for `DICE` model response.
    The counterfactuals only contain changed attributes.'''
    counterfactuals: List[CounterFactual] = Field(
        alias=counterfactuals, description="The <b>DICE</b> counterfactuals.")


class ExperimentInformation(BaseModel):
    '''JSON format for experiment creation.'''
    loan_ids: List[int]
    ismodify: bool
    iswhatif: bool  # Should only be True if ismodify is also true
    exp_type: ExplanationType
    experiment_name: str
    num_participants: Optional[int]
    survey_link: Optional[str] = Field(None, description="URL to a survey")
    description: Optional[str] = Field(
        None, description="description for the experiment")


class GenerateClientID(BaseModel):
    """JSON format for client ID generation request"""
    experiment_name: str


class ClientIDResponse(BaseModel):
    """JSON format for cliend id generation response. Integer from 0 upwards"""
    client_id: int = Field(ge=0)


class ExperimentResults(BaseModel):
    """JSON format for experiment results"""
    class SingleResult(BaseModel):
        loan_id: int = Field(ge=0, lt=1000)
        choice: RecommendationType
        timestamp: str
        modificationsCounter: int
        modifications: List[str]
        explanationsCounter: int
        explanations: List[str]

    experiment_name: str
    client_id: int
    results: List[SingleResult]
