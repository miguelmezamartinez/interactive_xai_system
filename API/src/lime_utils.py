import pandas as pd
import numpy as np
import lime
import lime.lime_tabular
from tensorflow.keras.models import load_model
from DataLoader_ey import data_loader 
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from constants import rename_dict, AttributeNames, lime_exp_mapping, attr_name, influence
import json

class LimeHelper():
    """Class for Lime Explanations.
    Uses code from xai_reference
    """
    def __init__(self):
        """Initializes the LimeHelper() for usage by the API
        Fits a preprocessor, label encoders and lime explainer
        """
        # Read credit data
        data = data_loader()
        self.data = data
        # Load tensorflow model
        self.model = load_model('smote_ey.tf')
        #steps from data_preprocess
        data.rename(columns=rename_dict, inplace=True)
        X_train = data.drop(columns='label')
        #steps from exp_preprocess
        feature_names = X_train.columns.to_list()
        cat_cols = X_train.select_dtypes(include=['object', 'category']).columns.to_list()
        num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.to_list()
        cat_indices = [feature_names.index(col) for col in cat_cols]
        cat_names = {}
        encoders = {}
        for cat_idx in cat_indices:
            # Fit label encoder on training data and transform respective column in training and test data
            le = LabelEncoder()
            le.fit(X_train.iloc[:, cat_idx])
            X_train.iloc[:, cat_idx] = le.transform(X_train.iloc[:, cat_idx])
            # Extend dictionary with array of categories and index as key
            cat_names[cat_idx] = le.classes_
            encoders[feature_names[cat_idx]] = le
                        
        preprocessor_le = ColumnTransformer(
                transformers=[('num', MinMaxScaler(), num_cols),
                            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)])
        preprocessor_le.fit(X_train)
        self.encoders = encoders
        self.prep = preprocessor_le
        self.X_train = X_train
        self.explainer = lime.lime_tabular.LimeTabularExplainer(X_train.values, feature_names=feature_names,
                                                    class_names=['Approved', 'Rejected'],
                                                    discretize_continuous=True, mode='classification',
                                                    categorical_features=cat_indices, categorical_names=cat_names,
                                                    feature_selection='lasso_path' )


    def predict_fn(self,X):
        """Prediction function for lime explainer
        :param X: should be the data without the column label
        """
        # Single data point has dimensions (18,) but (1, 18) is needed for preprocessing
        # Therefore, reshape input to (-1, 18)
        X_df = pd.DataFrame(X.reshape((-1, 18)), columns=self.X_train.columns)
        # Preprocess input and create nd-array
        X_transformed = self.prep.transform(X_df).toarray()
        # model.predict output has shape (n, 1) but (n,) is needed
        prob = self.model.predict(X_transformed).reshape(-1, )
        # Return predictions in correct format, dim = (n, 2), note that the first entry
        # has to represent P(y=0 | X)
        proba_predictions = np.array([1 - prob, prob]).transpose()
        return proba_predictions

    def preprocess_new_data(self, data):
        """
        Function to preprocess the given instance data for the lime explainer
        :param data: should be a pandas dataframe containing the attributes
        :return: label encoded data as a numpy array
        """
        feature_names = data.columns.to_list() 

        # Lists of categorical and numerical feature names (needed for preprocessing)
        cat_cols = data.select_dtypes(include=['object', 'category']).columns.to_list()

        # List of indices of categorical features
        cat_indices = [feature_names.index(col) for col in cat_cols]
        # Label encoding
        for cat_idx in cat_indices:
            #use the label encoders trained in __init__ to transform data
            le = self.encoders[feature_names[cat_idx]]
            data.iloc[:, cat_idx] = le.transform(data.iloc[:, cat_idx])
        
        #same order of columns as in the train data needs be assured
        correct_order_array = np.empty(len(feature_names))
        for key in lime_exp_mapping.keys():
            correct_order_array[key] = data.iloc[0, feature_names.index(lime_exp_mapping[key])]
        return correct_order_array

    def get_lime_exp(self, prediction_function, instance_df, num_features):
        """Method to get the lime explanation
        :param instance_df: dataframe with instance information
        :return lime explanation object:
        """
        data_le = self.preprocess_new_data(instance_df)
        lime_exp = self.explainer.explain_instance(data_le, prediction_function, num_features=num_features)
        return lime_exp
    
    def compute_response_lime(self,instance, num_features=6):
        """
        Method that can be called by the API after initializing the LimeHelper
        :param instance: given Instance info, should be in json format
        :return: a list of jsons with the keys attribute and influence
        """
        instance_df = pd.DataFrame(instance, index = [0])
        instance_df.drop(columns=["ident",AttributeNames.NN_recommendation.value,AttributeNames.NN_confidence.value], inplace=True) # TODO if pydantic model changes, this must change to!
        exp = self.get_lime_exp(self.predict_fn, instance_df, num_features)
        exp_dict = exp.__dict__
        #exp_dict also contains keys random_state,mode,domain_mapper,intercepts,score,local_pred,predict_proba, class_names,top_labels that are not needed
        local_exp = exp_dict['local_exp']
        local_exp_list = local_exp[1] #get list with explanation tuples from dict
        #create list of values with attribute names instead of numbers that are returned by lime
        lime_vals = []
        attributes_influence = 0
        for tuple in local_exp_list:
            dict = {}
            dict[attr_name] = lime_exp_mapping[tuple[0]]
            dict[influence] = tuple[1]
            attributes_influence += tuple[1]
            lime_vals.append(json.loads(json.dumps(dict)))
        # Modification
        # Add base value
        pred_proba = exp_dict['predict_proba'][1]

        #lime_bval = pred_proba - attributes_influence
        #lime_bval = pred_proba
        lime_bval = exp_dict['intercept'][1]
        
        return lime_vals, lime_bval
         
        




