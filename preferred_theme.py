# -*- coding: utf-8 -*-
"""Preferred_theme.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ctx5UnV57SnG_ixStP5Y1lci-gAm7gzH
"""

# Import relevent library

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.linear_model import LogisticRegression
import xgboost as xb

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.metrics import recall_score, confusion_matrix, precision_score, f1_score, accuracy_score, classification_report

# Load the train and test data
train =  pd.read_csv('/content/train.csv')
test = pd.read_csv('/content/test.csv')

# Read first five rows of data

train.head()

# Neglect special character value from singup date columns 
train['Sign_up_date'] = train['Sign_up_date'].replace(['?'],'2017-06-23')
# train = train[train.Sign_up_date != '?']

# Extract day ,year, momth from Sign_up_date
train['Sign_up_yyyy'] = pd.to_datetime(train['Sign_up_date']).dt.year
train['Sign_up_mm'] = pd.to_datetime(train['Sign_up_date']).dt.month
train['Sign_up_Day'] = pd.to_datetime(train['Sign_up_date']).dt.day

# Extract day ,year, momth from Last_order_placed_date
train['Last_order_placed_yyyy'] = pd.to_datetime(train['Last_order_placed_date']).dt.year
train['Last_order_placed_mm'] = pd.to_datetime(train['Last_order_placed_date']).dt.month
train['Last_order_placed_Day'] = pd.to_datetime(train['Last_order_placed_date']).dt.day

train.head()

# Neglect special character value from singup date columns 
test['Sign_up_date'] = test['Sign_up_date'].replace(['?'],'2016-01-01')
# test = test[test.Sign_up_date != '?']

# Extract day ,year, momth from Sign_up_date
test['Sign_up_yyyy'] = pd.to_datetime(test['Sign_up_date']).dt.year
test['Sign_up_mm'] = pd.to_datetime(test['Sign_up_date']).dt.month
test['Sign_up_Day'] = pd.to_datetime(test['Sign_up_date']).dt.day

# Extract day ,year, momth from Last_order_placed_date
test['Last_order_placed_yyyy'] = pd.to_datetime(test['Last_order_placed_date']).dt.year
test['Last_order_placed_mm'] = pd.to_datetime(test['Last_order_placed_date']).dt.month
test['Last_order_placed_Day'] = pd.to_datetime(test['Last_order_placed_date']).dt.day

# Checking missing values in train dataset

train.isnull().sum()

# fill the missing values in train data
train['Age'].fillna((train['Age'].mean()), inplace=True)
train['No_of_orders_placed'].fillna((train['No_of_orders_placed'].mean()), inplace=True)
train['Kid’s_Clothing'].fillna((train['Kid’s_Clothing'].mean()), inplace=True)
train['Home_&_Living'].fillna((train['Home_&_Living'].mean()), inplace=True)

# Checking missing values in train dataset

test.isnull().sum()

# fill the missing values in train data
test['Age'].fillna((test['Age'].mean()), inplace=True)
test['No_of_orders_placed'].fillna((test['No_of_orders_placed'].mean()), inplace=True)
test['Kid’s_Clothing'].fillna((test['Kid’s_Clothing'].mean()), inplace=True)
test['Home_&_Living'].fillna((test['Home_&_Living'].mean()), inplace=True)

# checking the shape of data
train.shape,test.shape

# Drop irrelevant columns from ther data set

train = train.drop(columns = ['CustomerID','State','Sign_up_date','Last_order_placed_date'])
test = test.drop(columns = ['CustomerID','State','Sign_up_date','Last_order_placed_date'])

"""# **EDA**"""

# summary of data

train.describe()

# checking the unique values in train dataset

train.nunique()

# count of Preferred_Theme
print(train.Preferred_Theme.value_counts(normalize = True))
print(train.Preferred_Theme.value_counts())

# count of is_premium_member
print(train.is_premium_member.value_counts(normalize = True))
print(train.is_premium_member.value_counts())

type_ = ["No", "Yes"]
fig = make_subplots(rows=1, cols=1)

fig.add_trace(go.Pie(labels=type_, values=train['is_premium_member'].value_counts(), name="is_premium_member"))

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name", textfont_size=16)

fig.update_layout(
    title_text="is_premium_member",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='is_premium_member', x=0.5, y=0.5, font_size=20, showarrow=False)])
fig.show()

# checking how many non -premium members gender wise
train.is_premium_member[train.is_premium_member == 0].groupby(by = train.Gender).count()

# checking how many premium members gender wise
train.is_premium_member[train.is_premium_member == 1].groupby(by = train.Gender).count()

type_ = ["New_UI", "Old_UI"]
fig = make_subplots(rows=1, cols=1)

fig.add_trace(go.Pie(labels=type_, values=train['Preferred_Theme'].value_counts(), name="Preferred_Theme"))

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name", textfont_size=16)

fig.update_layout(
    title_text="theme",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='Preferred_Theme', x=0.5, y=0.5, font_size=20, showarrow=False)])
fig.show()

# checking new_ui theme users  gender wise

train.Preferred_Theme[train.Preferred_Theme == "New_UI"].groupby(by = train.Gender).count()

# checking old_ui theme users  gender wise
train.Preferred_Theme[train.Preferred_Theme == "Old_UI"].groupby(by = train.Gender).count()

# One hot encoding
train = pd.get_dummies(train, columns = ['Gender','City','Sign_up_yyyy','Sign_up_mm','Sign_up_Day','Last_order_placed_yyyy','Last_order_placed_mm','Last_order_placed_Day'],prefix = '',prefix_sep = '')
test = pd.get_dummies(test, columns = ['Gender','City','Sign_up_yyyy','Sign_up_mm','Sign_up_Day','Last_order_placed_yyyy','Last_order_placed_mm','Last_order_placed_Day'],prefix = '',prefix_sep = '')

X = train.drop(labels=['Preferred_Theme'], axis=1)
y = train['Preferred_Theme'].values

from sklearn.model_selection import train_test_split
X_train, X_cv, y_train, y_cv = train_test_split(X, y, test_size=0.10, random_state=42)

X_train.shape, y_train.shape, X_cv.shape, y_cv.shape

# scaling the data
from sklearn.preprocessing import StandardScaler, MinMaxScaler
sc = StandardScaler()
X_train_sc = sc.fit_transform(X_train)
X_cv_sc = sc.fit_transform(X_cv)
test = sc.fit_transform(test)

# Logistic regression
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression() 
lr.fit(X_train_sc, y_train)

# predict on validation data
lr_pred = lr.predict(X_cv_sc)

from sklearn.metrics import accuracy_score, classification_report,confusion_matrix
print('Accuracy_score Testing Data: ',round(accuracy_score(y_cv, lr_pred)*100,2))
print('\n','Classification_report Testing data: ','\n','\n',classification_report(y_cv, lr_pred))

# XG Boost
xgb_model = xb.XGBClassifier(silent=False, 
                              scale_pos_weight=1,
                              learning_rate=0.1,
                              colsample_bytree =0.8,
                              subsample = 0.8,
                              objective='binary:logistic',
                              n_estimators=1000, 
                              max_depth=4, 
                              reg_alpha=0.01,
                              gamma=0,random_state=42)

# Model training
xgb_model.fit(X_train_sc, y_train,
              verbose=True)

# predict on validation data
RFpredict2 = xgb_model.predict(X_cv_sc)

print(accuracy_score(y_cv,RFpredict2))

print('\n','Classification_report Testing data: ','\n','\n',classification_report(y_cv, RFpredict2))

final_pred = xgb_model.predict(test)

# Random Forest
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train_sc,y_train)

RFpredict = model.predict(X_cv_sc)

print(accuracy_score(y_cv,RFpredict))
print(confusion_matrix(y_cv,RFpredict))
print(classification_report(y_cv,RFpredict))

test1 = pd.read_csv('/content/test.csv')

# Save the prediction results
submission = pd.DataFrame({
        "CustomerID": test1['CustomerID'],
        "Preferred_Theme": final_pred
    })
submission.to_csv('Preferred_ThemeSubmission3.csv', index=False)
print(submission)

"""1. final model used for prediction is XGBoost because its precision and recall are better than other models.

"""