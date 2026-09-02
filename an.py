import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(file_path):
    data_file = pd.read_csv(file_path, encoding="latin")
    data_file.columns = data_file.columns.str.strip().str.lower().str.replace(" ", "_")
    data_file["date"] = pd.to_datetime(data_file["date"], errors="coerce")

    return data

data_file = "supermarket_sales - Sheet1.csv"
data = load_data(data_file)

st.dataframe(data_file.head(7), hide_index=True)
