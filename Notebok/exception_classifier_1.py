# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 00:29:45 2018

@author: Karoonakar
"""

import os 
import json
import numpy as np
import pandas as pd
import dill as pickle
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier

from sklearn.pipeline import make_pipeline

import warnings
warnings.filterwarnings("ignore")

def build_and_train():
    path = 'data/exception_data.csv'
    dataFrame = pd.read_csv(path)
    
    df_master=dataFrame[["Module", "Language","Exception","CausedBy1","CausedBy2"]]
    df_lable=dataFrame[["Severity"]]
    df_message=dataFrame[["Message"]]
    df_causedBy1Msg=dataFrame[["CausedBy1Msg"]]
    df_causedBy2Msg=dataFrame[["CausedBy2Msg"]]



class PreProcessing(BaseEstimator, TransformerMixin):
    """Custom Pre-Processing estimator
    """

    def __init__(self):
        vect_msg = CountVectorizer(ngram_range=(2, 3))
        vect_causedby1_msg = CountVectorizer(ngram_range=(2, 3))
        vect_causedby2_msg = CountVectorizer(ngram_range=(2, 3))
        

    def transform_msg(self, df_message):
        msg_train_dtm = self.vect_msg.fit_transform(df_message.Message)
        message_trigramed_frame= pd.DataFrame(msg_train_dtm.toarray(),columns=self.vect_msg.get_feature_names())
    
        return message_trigramed_frame

    def transform_causedBy1Msg(self, df_causedBy1Msg):
        msg_causedby1_train_dtm = self.vect_causedby1_msg.fit_transform(df_causedBy1Msg.CausedBy1Msg)
        causedby1_msg_trigramed_frame=pd.DataFrame(msg_causedby1_train_dtm.toarray(),columns=self.vect_causedby1_msg.get_feature_names())
    
        return causedby1_msg_trigramed_frame;

    def transform_causedBy2Msg(self, df_causedBy2Msg):
        msg_causedby2_train_dtm = self.vect_causedby2_msg.fit_transform(df_causedBy2Msg.CausedBy2Msg)
        causedby2_msg_trigramed_frame=pd.DataFrame(msg_causedby2_train_dtm.toarray(),columns=self.vect_causedby2_msg.get_feature_names())
    
        return causedby2_msg_trigramed_frame;

    def transform(self, df_master,df_message, df_causedBy1Msg,df_causedBy2Msg):
        df1=pd.merge(df_master, self.transform_msg(df_message), left_index=True, right_index=True)
        df2=pd.merge(df1, self.transform_causedBy1Msg(df_causedBy1Msg), left_index=True, right_index=True)
        df3=pd.merge(df2, self.transform_causedBy2Msg(df_causedBy1Msg), left_index=True, right_index=True)
        
        return def3;
        
    def get_vect_msg(self):
        return self.vect_msg
    
    def get_vect_causedby1_msg(self):
        return self.vect_causedby1_msg
    
    def get_vect_causedby2_msg(self):
        return self.vect_causedby2_msg
    
    
if __name__ == '__main__':
	model = build_and_train()

	filename = 'exception_classifier.pk'
	with open('models/'+filename, 'wb') as file:
		pickle.dump(model, file)