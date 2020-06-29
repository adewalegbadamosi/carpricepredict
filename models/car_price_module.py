#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# This module assume linearity of the input data and LinearRegression model is adopted

# import all libraries needed

import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression


# create the car price class

class CarPrice():
    
    # create the constructor
    def __init__(self,model,scaler,buffer):
        
        with open(model,'rb') as model_file, open(scaler,'rb') as scaler_file:
            self.reg = pickle.load(model_file)
            self.scaler = pickle.load(scaler_file)
            
        self.buffer = pd.read_csv(buffer, delimiter=',')
        self.preprocessed_input = None 
        self.user_data_length = None
        
    # create the data_preprocessing method
    def data_preprocessing(self, data):
        
        if type (data) == list:
            self.buffer.loc[0] = data
            self.raw_data = self.buffer.copy()
        else:
            user_data = pd.read_csv(data, delimiter=',')
            self.user_data_length = len(user_data)         
            bufferred_data = pd.concat([user_data, self.buffer], ignore_index=True)
            self.raw_data = bufferred_data.copy()
     
            
        # replcae all empty data points with 1       
        data_null_screened = self.raw_data.fillna(1)

        # rearrange data_null_screened and put price at the end
        data_null_screened = data_null_screened[['Brand', 'Body', 'Mileage', 'EngineV', 'Engine Type',
       'Registration', 'Year', 'Model','Price']]
        self.data_null_screened = data_null_screened.copy()
        data_with_Registration_mapped = data_null_screened.copy()
        
        # map the Registration column yes:1 no:0
        data_with_Registration_mapped['Registration'] = np.where(data_null_screened['Registration'] == 'yes',1,0)
        # get dummies for all the relevant categorical data ie Brand,Body,Engine Type
        data_with_dummies = pd.get_dummies(data_with_Registration_mapped, columns= ['Brand','Body','Engine Type'], drop_first=True)
        # get input for the model by droping the irrelivant columns
        input_ = data_with_dummies.drop(['EngineV','Model','Price'], axis=1)
        self.unstandardized_input = input_.copy()
        
                
        # Standardize the input with the scalar object        
        standardized_input = self.scaler.fit_transform(input_)    # transforming the input values to standardized form
        
        # store standardized_input as class attribute for other use
        self.preprocessed_input = standardized_input.copy()
             
    # create price prediction method
    def price_predicted(self):
        
        if  self.preprocessed_input is not None :
            predicted_price = np.exp(self.reg.predict(self.preprocessed_input))   
            
            #convert output to list
            predicted_price = [ round(i,2) for i in list(predicted_price) ]
                        
            if self.user_data_length:
                user_predicted_price = []
                for i in range(self.user_data_length):
                    user_predicted_price.append(predicted_price[i])
                return user_predicted_price
            else:
                return predicted_price[0]
        
    # create prediction table for further business intelligence analysis
    def price_prediction_table(self):
        
        if  self.preprocessed_input is not None :
            
            predicted_price = np.exp(self.reg.predict(self.preprocessed_input)) 
            price_prediction_table = self.data_null_screened.copy()
            price_prediction_table['predicted_price'] = predicted_price
            price_prediction_table['predicted_price'] = round( price_prediction_table['predicted_price'], 2 )
            
        # return table for only the length of user data   
        if self.user_data_length:
            return price_prediction_table.iloc[: self.user_data_length ]
        else:
            return price_prediction_table.iloc[: 1]

        
        
         

