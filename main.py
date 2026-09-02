import streamlit as st
import pandas as pd

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [23, 30, 37]
}

df = pd.DataFrame(data)

st.write("### Using st.write() for Dataframe")
st.write(df)

st.write("Static Table")
st.table(df)

st.write("Interactive Dataframe")
st.dataframe(df)

person = {
    "name": "Alice",
    "age": 25,
    "skills": ["Python", "Streamlit", "Data science"]
}

st.json(person)
st.write("dictionary displayed with st.write():", person)