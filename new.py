import streamlit as st

st.title("Desmond's Web App Interface")

st.header("Warmly Welcome to Desmond's Web App Interface")

st.subheader("In God We Trust")

st.set_page_config(page_title="Desmond's Interface", layout="wide")

st.info("This is a simple web app interface created using Streamlit. You can use this interface to display various messages and information.")

user_name = st.text_input("Enter your name")

if user_name:
    st.write(f"Hello, {user_name.upper()}")
else:
    st.write("Please enter your name above.")

print("Scipt Executed")