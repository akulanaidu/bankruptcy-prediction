# -*- coding: utf-8 -*-
"""bankruptcy deploy.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ayWDQLzAN4iSdpMyQdRtG45JjJCxTpFS
"""
import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression

st.title('Bankruptcy Prevention')

st.sidebar.header('User Input Parameters')

def user_input_features():
    industrial_risk = st.sidebar.selectbox('industrial_risk', ('0', '0.5', '1.0'))
    management_risk = st.sidebar.selectbox('management_risk', ('0', '0.5', '1.0'))
    financial_flexibility = st.sidebar.selectbox('financial_flexibility', ('0', '0.5', '1.0'))
    credibility = st.sidebar.selectbox('credibility', ('0', '0.5', '1.0'))
    competitiveness = st.sidebar.selectbox('competitiveness', ('0', '0.5', '1.0'))
    operating_risk = st.sidebar.selectbox('operating_risk', ('0', '0.5', '1.0'))
    data = {
        'industrial_risk': industrial_risk,
        'management_risk': management_risk,
        'financial_flexibility': financial_flexibility,
        'credibility': credibility,
        'competitiveness': competitiveness,
        'operating_risk': operating_risk
    }
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()
st.subheader('User Input parameters')
st.write(df)

# Load your dataset
bankrupt_new = pd.read_csv("bankruptcy-prevention.csv")

# Clean column names in the dataset
bankrupt_new.columns = bankrupt_new.columns.str.strip()

# Convert the feature columns to float
for col in bankrupt_new.columns[:-1]:  # Exclude the 'class' column
    bankrupt_new[col] = bankrupt_new[col].astype(float)

# Convert 'class' column to binary
bankrupt_new['class'] = bankrupt_new['class'].apply(lambda x: 1 if x == 'bankruptcy' else 0)



# Define the target variable (update the column name if it's different)
target_variable = 'class'  # Ensure this matches the actual target column name

if target_variable not in bankrupt_new.columns:
    st.error(f"Target variable '{target_variable}' not found in the dataset. Please check the column names.")
else:
    # Separate the target variable and features
    y = bankrupt_new[target_variable]
    X = bankrupt_new.drop(columns=[target_variable])

    # Ensure the columns in the user input match the training data
    df = df[X.columns]

    # Train the logistic regression model
    clf = LogisticRegression()
    clf.fit(X, y)

    # Add a Predict button
    if st.button('Predict'):
        # Make predictions
        prediction = clf.predict(df)
        prediction_proba = clf.predict_proba(df)

        # Display results
        st.subheader('CLASS Prediction')
        st.write('The company is predicted to go bankrupt.' if prediction[0] == 1 else 'No, the company is not going to be bankrupt')

        st.subheader('Prediction Probability')
        st.write(prediction_proba)
