import streamlit as st

if st.button("click Me"):
    st.write("button clicked")

choice = st.radio("Choose an option", ["Billy Strings", "Nine Inch Nails", "Trivium"])
st.write("You selected:", choice)

agree = st.checkbox("I agree")
if agree:
    st.write("Thanks for agreeing!.")

    #functions learning
    import streamlit as st

genre = st.selectbox("pick a genre:", ['Gospel', "Reggae", "Highlife"])
st.write('Your favourite Genre is:', genre)

reggae_subgenre = st.multiselect("pick your favourite reggae genre:", ["Roots", "Dancehall", "Dub"])
st.write("Your favourite reggae genres are:", reggae_subgenre)

# functions of input
age = st.slider("select your age:", 1, 20, 100)
st.write("Age", age)

number = st.number_input("Enter a number")
st.write("Number: ", number)

name = st.text_input("Enter your name")
st.write("Hello: ", name)

bio = st.text_area("Write a short bio:")
st.write("Your bio: ", bio)

date = st.date_input("Pick a date")
st.write("Selected date:", date)

time = st.time_input("Pick a time")
st.write("Time selected:", time)

# file uploading tackling
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    st.text_area("File Content:", content, height=200)

    