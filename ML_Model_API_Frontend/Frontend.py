import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Health Insurance Category")

occupation_list = [
    'retired', 'freelancer', 'student', 'government_job',
    'business_owner', 'unemployed', 'private_job'
]

city_list = [
    'Jaipur', 'Chennai', 'Indore', 'Mumbai', 'Kota',
    'Hyderabad', 'Delhi', 'Chandigarh', 'Pune',
    'Kolkata', 'Lucknow', 'Gaya',
    'Jalandhar', 'Mysore', 'Bangalore'
]


with st.form("prediction_form"):

    age = st.number_input("Age", min_value=1,max_value=100)
    weight = st.number_input("Weight (kg)", min_value=1.0)
    height = st.number_input("Height (cm)", min_value=1.0)
    income_lpa = st.number_input("Income (LPA)", min_value=0.0)

    smoker = st.selectbox("Smoker", ["Yes", "No"])
    occupation = st.selectbox("Occupation", occupation_list)
    city = st.selectbox("City", city_list)

    submit = st.form_submit_button("Predict")


if submit:
    payload = {
        "age" : age,
        "weight" : weight,
        "height" : height,
        "income_lpa" : income_lpa,
        "smoker" : smoker,
        "city" : city,
        "occupation" : occupation
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=5
        )

        st.write(f"Response status code: {response.status_code}")

        try:
            result = response.json()  # try parse JSON
        except Exception:
            st.error("Response is not JSON!")
            st.write(response.text)
            result = None

        if response.status_code == 200 and result is not None:
            # Use .get() to avoid KeyError
            predicted = result.get('predicted_category', result)
            st.success(f"Predicted Insurance Premium Category: **{predicted}**")
            st.json(result)
        else:
            st.error(f"Error: {response.status_code}")
            st.write(response.text)

    except requests.exceptions.RequestException as e:
        st.error("API not reachable")
        st.write(str(e))
