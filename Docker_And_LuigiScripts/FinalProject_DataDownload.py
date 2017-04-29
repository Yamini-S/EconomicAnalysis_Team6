import pandas as pd
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import math
import os
import glob
from datetime import datetime
import itertools
#import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARMA
from sklearn import preprocessing
import operator
import numpy as np
import xlrd



def returnCleanedListOfDF(df_list_input):
    pathToCSV = './bins'
    if not os.path.exists(pathToCSV):
        os.makedirs(pathToCSV)
    os.chdir(pathToCSV)    
    df_list_out = []
    for df_in_list_input in df_list_input:
        indicator_name, state_name, df_in_list = df_in_list_input
        df_list_new = df_in_list.dropna(how='all')
        matrix_new = df_list_new[df_list_new.columns].as_matrix()
        matrix_new_transposed = matrix_new.transpose()
        df_new = pd.DataFrame(data=matrix_new_transposed)
        df_new.columns = df_new.iloc[0]
        df_new = df_new[1:]

        statefound = True
        two_col_df = pd.DataFrame()
        for a in df_new.columns:
            if isinstance(a, float) and statefound:
                # print(df_new.ix[:,0])
                two_col_df['Year'] = df_new.ix[:, 0].astype(int).astype('str')
                statefound = False
            elif isinstance(a, str) and a.find("Statewide") != -1:
                print('====')
                print(indicator_name)
                print(state_name)
                print(a)
                two_col_df[state_name + '_' + indicator_name] = df_new[a]

        two_col_df.to_csv(state_name + '_' + indicator_name + '.csv', index=False)
        df_list_out.append((indicator_name, state_name, two_col_df))
        print(df_in_list.shape)
    return df_list_out

def driver():
    anchor_tag_name = ['House Price Index', 'Unemployment Rate (Household Survey)', 'Total Personal Income',
                       'Gross State Product (Real)']
    sheet_names = ['DC', 'MD', 'NC', 'SC', 'VA']
    url = 'https://www.richmondfed.org/research/regional_economy/reports/regional_profiles#tab-2'
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    selected_tag = soup.findAll("a")
    base_url = 'https://www.richmondfed.org'
    list_urls = []
    for tag_name in anchor_tag_name:
        for selected in selected_tag:
            if selected.string == tag_name:
                print(base_url + selected['href'])
                list_urls.append((tag_name, base_url + selected['href']))
    df_list = []
    for url_link in list_urls:
        indicator_name, indicator_url = url_link
        indicator_name = indicator_name.replace(" ","")
        for each_sheet in sheet_names:
            df_dc = pd.read_excel(indicator_url, sheetname=each_sheet)
            df_list.append((indicator_name, each_sheet, df_dc))
        print(len(df_list))
    df_list_new = returnCleanedListOfDF(df_list)
    return df_list_new




def handleMissingData(df):
    df = df.fillna(df.bfill())
    return df

def logTransform(df):
    ts_log = np.log(df)
    return ts_log


def cal_aic_metric(modelname,model):
    aic_metric = pd.DataFrame({'Modelname':[],'AIC':[]})
    aic_dict = {}
    global aic_metric
    AIC = model.aic
    aic_dict[modelname] = AIC
    df_error = pd.DataFrame({'Modelname':[modelname],'AIC':[AIC]})
    aic_metric = pd.concat([aic_metric,df_error]) 
    #aic_metric.to_csv('AICMetric.csv', sep=",",mode='a')
    return aic_metric



def AR_Model(ts, param):   
    model = ARMA(ts, order=param)
    results_AR = model.fit(disp=0)
    print("Model AIC:",results_AR.aic)
    modelmetric = cal_aic_metric(param,results_AR)
    return results_AR

def FinalAR_Model(ts, param):   
    model = ARMA(ts, order=param)
    results_AR = model.fit(disp=0)
    print("Model AIC:",results_AR.aic)
    #cal_aic_metric(param,results_AR)
    return results_AR


def forecast(model,numSteps):
    pathToOutputFiles = './OutputFiles'
    output = model.forecast(steps=numSteps)[0]
    output.tolist()
    output = np.exp(output)
    #ForecastOutput=pd.DataFrame(output, columns=['forcasts']).to_csv(pathToOutputFiles+'/'+'ForecastedValues.csv',mode='a')
    ForecastOutput=pd.DataFrame(output, columns=['forcasts']).to_csv(pathToOutputFiles+'/' +'ForecastedValues.csv',mode='a')
    print('Forecasted values are:',output)
    #print(output)
    return output

def FittedValues(model):
    pathToOutputFiles = './OutputFiles'
    fittedVal=model.fittedvalues
    PredictedVal=np.exp(fittedVal)
    prediction = pd.DataFrame(PredictedVal, columns=['predictions']).to_csv(pathToOutputFiles+'/'+'PredictedValues.csv',mode='a')
    #prediction = pd.DataFrame(PredictedVal, columns=['predictions']).to_csv(pathToOutputFiles+'/'+'PredictedValues.csv',mode='a')
    print('Predicted existing values are:',PredictedVal)
    return PredictedVal


def chooseModel(df_log):
    p = range(0, 2)
    q = range(0,1)
    pq = list(itertools.product(p, q))
    for param in pq:
        results=AR_Model(df_log, param)
    print(aic_metric)
    #aic_metric.to_csv('AICMetric.csv', sep=",",mode='a')
    paramNew=aic_metric['Modelname'][aic_metric['AIC']==aic_metric['AIC'].min()]
    paramNew=paramNew[0]
    print('Model selected:')
    print(paramNew)
    results_AR_final=FinalAR_Model(df_log, paramNew)
    output_forecast = forecast(results_AR_final, 10)
    predictedValues = FittedValues(results_AR_final)
    return output_forecast

def readFile(filename):
    #os.chdir('./bins')
    print(os.getcwd())
    df_1 = pd.read_csv(filename, header=0,parse_dates=['Year'],index_col=0)
    df_2 = pd.DataFrame(df_1)
    pd.to_datetime(df_2.index,format='%Y')
    df_2 = df_2.set_index(pd.DatetimeIndex(df_2.index))
    print("File read is:",filename)
    print(df_2.shape)
    df_2 = df_2.sort()
    df_2 = handleMissingData(df_2)
    print("Missing data handled")
    ts_log = logTransform(df_2)  
    print("Log Transform done")
    #aic_metric = pd.DataFrame({'Modelname':[],'AIC':[]})
    #aic_dict = {}
    result = chooseModel(ts_log)
    return df_2

def ReadFileAndExecuteModels():
    pathToOutputFiles = './OutputFiles'
    if not os.path.exists(pathToOutputFiles):
        os.makedirs(pathToOutputFiles)
    count=0
    print(os.getcwd())
    for (dirname, dirs, files) in os.walk('.'):
        print(files)
        print(os.getcwd())
        for file_ in files:
            try:
                if file_.endswith('.csv'):
                    projectFile = readFile(file_)
                    count = count + 1 
                else:
                    print("There are no CSV Files to read ")
            except Exception as e:
                print(e)
                print("Files not found")
    print("Total files found:\t", count)
