import json
import joblib
import pandas as pd
import streamlit as st

options = json.load(open('options.json'))
st.header("Car Price Predictor")

tree, X_columns = joblib.load('car_price_predictor.pkl')


def predict_price(i):
    dummies = pd.get_dummies(pd.DataFrame([i]))
    for column in dummies.columns:
        if column not in X_columns:
            del dummies[column]
    df = pd.DataFrame(dummies, columns=X_columns)
    return tree.predict(df)[0]


def predict():
    i = {
        'Name': st.session_state.model,
        'Manufacturer': st.session_state.manufacturer,
        'Year': st.session_state.year,
        'Location': st.session_state.location,
        'Kilometers_Driven': st.session_state.km,
        "Fuel_Type": st.session_state.fuel,
        "Transmission": st.session_state.transmission,
        "Owner": st.session_state.owner,
        "Engine CC": st.session_state.cc,
        "Power": st.session_state.power,
        "Seats": st.session_state.seats
    }
    price = predict_price(i)
    # print({**i, 'Price': price})
    st.session_state.price = price


st.selectbox(
    "Manufacturer",
    options=options['manufacturers'],
    placeholder="Select a manufacturer",
    key="manufacturer",
    on_change=predict
)

st.selectbox(
    "Model",
    options=options['models'][st.session_state.manufacturer],
    placeholder="Select a model",
    key="model",
    on_change=predict
)

st.selectbox(
    "Year",
    options=range(
        options['years'][st.session_state.manufacturer]['min'],
        options['years'][st.session_state.manufacturer]['max']+1
    ),
    placeholder="Select a year",
    key="year",
    on_change=predict
)

st.selectbox(
    "Location",
    options=options['locations'],
    placeholder="Select a location",
    key='location',
    on_change=predict
)

st.slider(
    "Kilometers driven",
    min_value=options['km']['min'],
    max_value=options['km']['max'],
    step=100,
    format='%dkm',
    key='km',
    on_change=predict
)

st.selectbox(
    "Fuel Type",
    options=options['fuel_type'],
    key='fuel',
    on_change=predict
)

st.selectbox(
    "Transmission type",
    options=options['transmission'],
    key="transmission",
    on_change=predict
)

st.selectbox(
    "Owner type",
    options=options['owner_type'],
    key="owner",
    on_change=predict
)

st.slider(
    "Engine capacity",
    min_value=options['engine_cc']['min'],
    max_value=options['engine_cc']['max'],
    step=5,
    format='%dcc',
    key='cc',
    on_change=predict
)

st.slider(
    "Power",
    min_value=options['power']['min'],
    max_value=options['power']['max'],
    step=5,
    key='power',
    on_change=predict
)

st.slider(
    "Number of seats",
    min_value=options['seats']['min'],
    max_value=options['seats']['max'],
    key='seats',
    on_change=predict
)

predict()
st.success(f"Price: {st.session_state.price}")
