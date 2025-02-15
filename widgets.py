import streamlit as st
import pandas as pd
import time
# Text input

name = st.text_input("Enter your name:")
if name: 
    st.write(f"Hello {name}")

x = st.number_input("Enter a number", min_value=1, max_value=99, step=1)


# Number
st.write(f"The number is {x=}")

# Divider
st.divider()

# Button

if st.button("Click me !"):
    st.write(":ghost:"*3)

# Checkbox

agree = st.checkbox("I agree")
if agree:
	st.success("Great !")
     
df = pd.DataFrame({
	"Name":["Anne","Mario","Douglas"],
	"Age": [30, 25, 40]
})

if st.checkbox("Show Data"):
	st.write(df)
      
options_list = ["Cat", "Dog","Fish", "Turtle"]
pet = st.radio("Choose an animal", options=options_list, index=2, key="your_pet") # index is the default checked when starting the app
 
 
st.write(f"You favourite animal is {pet}")
st.write(f"The selected value is {st.session_state.your_pet}") # defining widget by key is like defining a sesssion state

# Select
cities = ["London", "Paris", "Berlin", "Madrid"]
city = st.selectbox("Your city", cities)

st.write(f"You live in {city}")

st.divider()

# Slider

x = st.slider("x", 
              value=15,
              max_value=400,
              min_value=20
              ) # value = default value and between 0 and 100 if not said otherwise
st.write(f"{x=}")

# file uploader
allowed_extensions = ["txt", "csv", "xlsx", "pdf"]
uploaded_file = st.file_uploader("Upload file", type=allowed_extensions) # by default 200Mb that we can configure using server.maxUploadSize config


if uploaded_file:
	st.write(uploaded_file)
	if uploaded_file.type == "text/csv":
		df = pd.read_csv(uploaded_file)
		st.write(df)
		
# Camera input
#camera_photo = st.camera_input("Take a photo")
#if camera_photo:
#	st.image(camera_photo)

# Sidebar

my_select_box = st.sidebar.selectbox("Select", ["US","UK","DE"])
my_slider = st.sidebar.slider("Temperature")

st.divider()

left_col, right_col = st.columns(2)

import random as rd

data = [rd.random() for _ in range(100)]

# we can use a context manager or calling method directly 

with left_col:
	st.subheader("A linechart")
	st.line_chart(data)
	

right_col.subheader("Data")
right_col.write(data[:10])

col1, col2, col3 = st.columns([0.2, 0.5, 0.3]) # creates three columns + size in percentage of the total size !

col1.markdown("Hello Streamlit")
col2.write(data[5:10])
with col3:
	st.header("A cat")
	st.image("https://www.google.com/imgres?q=cat..")
	
# Expander

with st.expander("Click to expand"):
	st.bar_chart({"Data":[rd.randint(2,10) for _ in range(25)]})
	

st.write("Starting an extensive computaiton ... ")
latest_iteration = st.empty() # place holder to hold element that can be updated !

progress_text = "Operation in progress. Please wait ... "

my_bar = st.progress(0, text  = progress_text)
time.sleep(2)

#for i in range(100):
#	my_bar.progress(i+1)
#	latest_iteration.text(f"Iteration {i+1}")
#	time.sleep(0.1)

#st.write("We are done: :smile:")

st.write(st.session_state)


if "counter" not in st.session_state:
    st.session_state["counter"] = 0
else:
    st.session_state.counter += 1
    
st.write(f"Counter {st.session_state.counter}")

button = st.button("Update state")
if "clicks" not in st.session_state:
	st.session_state["clicks"] = 0
if button:
	st.session_state.clicks += 1
st.write(st.session_state["clicks"])

number = st.slider("Value", 1, 10, key="my_slider") #using key argument link the variable to the session state !!!!

st.write(st.session_state)

# Callbacks

st.subheader("Distance converter")

def miles_to_km():
	st.session_state.km = st.session_state.miles*1.609
	
def km_to_miles():
	st.session_state.miles = st.session_state.km*0.621

col1, buff, col2 = st.columns([2, 1, 2])
with col1:
	miles = st.number_input("Miles:", key="miles", on_change=miles_to_km)
	
	
with col2:
	km = st.number_input("Km:", key="km", on_change=km_to_miles)