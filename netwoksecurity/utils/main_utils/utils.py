import yaml
import dill
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging
import os,sys
import numpy as np
import pickle
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import StratifiedKFold


from sklearn.metrics import f1_score









def read_yaml_file(file_path):
    try:
        with open (file_path , 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise CustomException(e,sys)
    
def write_yaml_file(file_path , content , replace:bool = False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path , "w") as file:
            return yaml.dump(content ,file)
    
    except Exception as e:
        raise CustomException(e,sys)
    

def save_numpy_array(file_path:str, array:np.array): 
    ''' 
    save numpy array in .npy format using 
    np save function.
    '''
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path , "wb") as file:
            np.save(file , array)
    except Exception as e:
        raise CustomException(e,sys)
    
def save_pikle(file_path:str,obj:object):
    try:
        logging.info("saving my pikle file")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
        logging.info("pikle file saved")
    except Exception as e:
        raise CustomException(e,sys)
    
def save_obj(file_path:str, obj:object):
    try:
        logging.info("saving object in utils file")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path ,  exist_ok= True)
        with open(file_path ,"wb") as file:
            return pickle.dump(obj,file)
        logging.info("saved file")

    except Exception as e:
        raise CustomException(e,sys)
    
def load_obj(file_path:str):
    try:
        if not(os.path.exists(file_path)):
            raise Exception(f"The file {file_path} donot exist")
        with open(file_path,"rb") as file:
            return pickle.load(file)
    except Exception as e:
        raise CustomException(e,sys)
    
def load_numpy_array(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} donot exist")
        with open(file_path,"rb") as file:
            return np.load(file)
    except Exception as e:
        raise CustomException(e,sys)
        
def eval_model(x_train,y_train,x_test,y_test,models:dict , params:dict):
    my_models  = list(models.values())
    params = list(params.values())
    model_keys = list(models.keys())
    report:dict = {}
    trained_model:dict = {}
    cv_strategy = StratifiedKFold(n_splits=2, shuffle=True, random_state=42)

    try:
        for i in range(len(my_models)):
            curr_model = my_models[i]
            search = RandomizedSearchCV(estimator=my_models[i] , param_distributions=params[i] , cv=cv_strategy, error_score='raise')
            search.fit(x_train,y_train)
            best_param = search.best_params_
            curr_model.set_params(**best_param)
            curr_model.fit(x_train,y_train)
            y_train_pred = curr_model.predict(x_train)
            y_test_pred = curr_model.predict(x_test)

            train_score = f1_score(y_train,y_train_pred)
            test_score = f1_score(y_test,y_test_pred)

            report[model_keys[i]] = test_score
            trained_model[model_keys[i]] = curr_model
            
        return report , trained_model

    except Exception as e:
        raise CustomException(e,sys)





