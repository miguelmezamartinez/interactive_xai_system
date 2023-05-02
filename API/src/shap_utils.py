import pandas as pd
from constants import AttributeNames
from DataLoader_ey import data_loader
from tensorflow.keras.models import load_model
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from models import InstanceInfo
from constants import inv_rename, rename_dict
import shap

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

class ShapHelperV2: # TODO load model only once for each process (pass it to the explainers!)
    def __init__(self):
        """TODO"""
        self.model = load_model("smote_ey.tf")
        self.data = data_loader()
        self.X_train = None
        self.train_data = None
        self.test_data = None
        self.X_train = None
        self.X_test = None
        self.preprocessor = None

    def prepare_shap(self):
        """TODO mainly taken from explanation_utils_ey"""
        self.data.rename(columns=rename_dict, inplace=True)
        X = self.data.drop(columns='label') # feature matrix
        y = self.data['label'] # target array
        # Create train and test split
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
        self.train_data = X_train.join(pd.DataFrame(y_train, columns=['label']))
        self.test_data = X_test.join(pd.DataFrame(y_test, columns=['label']))
        self.X_train = self.train_data.drop(columns='label')
        self.X_test = self.test_data.drop(columns='label')

        num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cat_cols = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
        preprocessor = ColumnTransformer(
            transformers=[('num', MinMaxScaler(), num_cols),
                          ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)]
        )
        preprocessor.fit(X_train)
        self.preprocessor = preprocessor

    def get_pred_fn(self):
        """TODO"""

        def predict_fn(X):
            X_df = pd.DataFrame(X.reshape((-1, 18)), columns=self.X_train.columns)
            X_transformed = self.preprocessor.transform(X_df).toarray()
            result = self.model.predict(X_transformed).flatten()
            return result
        
        return predict_fn
    
    def predict_shap(self, X): # TODO rename
        X_df = pd.DataFrame(X.reshape((-1, 18)), columns=self.X_train.columns)
        X_transformed = self.preprocessor.transform(X_df).toarray()
        result = self.model.predict(X_transformed).flatten()
        return result

def get_pred_fn_helper(helper: ShapHelperV2):
    def predict_fn(X):
        X_df = pd.DataFrame(X.reshape((-1, 18)), columns=helper.X_train.columns)
        X_transformed = helper.preprocessor.transform(X_df).toarray()
        result = helper.model.predict(X_transformed).flatten()
        return result
    return predict_fn

#Modification backup
#Add shap explainer to try to extract prediction probability from model
#def compute_response_shap(instance : InstanceInfo, explainer : shap.KernelExplainer, cols: list, sh: ShapHelperV2, num_features=18, ):
def compute_response_shap(instance : InstanceInfo, explainer : shap.KernelExplainer, cols: list, num_features=18, ):
    data_dict = {col : [instance.__dict__[col]] for col in cols}
    data_for_explainer = pd.DataFrame(data_dict)
    
    shap_vals = explainer.shap_values(data_for_explainer, nsamples=500, l1_reg=f"num_features({num_features})")
    shap_bval = explainer.expected_value

    #pred_proba = sh.model.predict(sh.preprocessor.transform(data_for_explainer))[0][0]
    #pred_proba = instance.NN_confidence
    #recomendation = instance.NN_recommendation

    #return shap_bval, shap_vals, pred_proba, recomendation
    return shap_bval, shap_vals

# Do not Use
class OLD_ShapHelper:
    def __init__(self):
        # load dataset
        data = data_loader()
        data = data.drop(columns="label")
        # numerical column names
        numericals = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        # categorical column names
        categoricals = data.select_dtypes(include=['object', 'category']).columns.tolist()

        preprocessor_shap = ColumnTransformer(
            transformers=[
                ('num', MinMaxScaler(), numericals),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categoricals)
            ]
        )
        preprocessor_shap.fit(data)

        self.pre = preprocessor_shap

        model = load_model('smote_ey.tf')
        def predict_fn_shap(X):
            # Single data point has dimensions (18,) but (1, 18) is needed for preprocessing
            # Therefore, reshape input to (-1, 18)
            X_df = pd.DataFrame(X.reshape((-1,18)), columns=[e.value for e in AttributeNames if e not in [AttributeNames.NN_confidence, AttributeNames.NN_recommendation, AttributeNames.ident]])
            # Preprocess input and create nd-array
            X_transformed = preprocessor_shap.transform(X_df).toarray()
            # model.predict output has shape (n, 1) but (n,) is needed
            prob = model.predict(X_transformed).reshape(-1,)
            return prob
        self.explainer = shap.KernelExplainer(predict_fn_shap, preprocessor_shap.transform(data))

    def transform(self, df: pd.DataFrame):
        return self.pre.transform(df)

    def transform_API_response(self, instance: InstanceInfo):
        '''Returns the API response for a dataset instance (loan application) as a transformed dataFrame preprocessed for Shap'''
        needed_attrs = [e.value for e in AttributeNames if e not in [AttributeNames.NN_confidence, AttributeNames.NN_recommendation, AttributeNames.ident]]
        df_dict = {}
        # use correct attribute names for model
        for name in needed_attrs:
            df_dict[inv_rename[name]] = [instance[name]]
        df = pd.DataFrame(df_dict)
        return self.transform(df)