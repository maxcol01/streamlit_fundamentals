import streamlit as st
import pandas as pd
import time

st.title("Hello Streamlit World: :smile:")

# Displaying data on the screen::
# 1. st.write()
# 2. Magic

st.write("We are learning Streamlit")


l1 = [1, 2, 3]
st.write(l1)

l2 = list("abc")
d1 = dict(zip(l2,l1))
st.write(d1)

# using magic: automatically write this to the screen

"Displaying using Magic"


# Dataframe

df = pd.DataFrame({
	"first column": [1,2,3,4],
	"second column": [10, 20, 30, 40]
})
df