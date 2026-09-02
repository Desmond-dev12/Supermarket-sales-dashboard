import streamlit as st

st.title("Session State Demo")

if "Counter" not in st.session_state:
    st.session_state.counter=0

if st.button("Increment"):
        st.session_state.counter +=1

st.write("Couter value:", st.session_state.counter)