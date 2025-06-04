import streamlit as st
import pandas as pd
from collections import Counter
import folium 
from streamlit_folium import st_folium

# Create a header to introduce our users 
st.title("Chicago Food Inspection Map")

df = pd.read_csv("data/clean_food_inspections.csv")

# Create a non null, unique, list of zip code options
zip_options = df["Zip"].dropna().unique().tolist()

# Create a subheader to direct user input
st.sidebar.subheader("Zip Code Filter")

# Creating a hybrid
user_zip = st.sidebar.text_input("Enter a Zip Code (optional):")
dropdown_zip = st.sidebar.selectbox("Or select one:", ["All"] + zip_options)

# Add an option to only view failed health inspection results
fail_only = st.sidebar.checkbox("Show only failed inspections", value = False)

# Filters through user input first, then box selection, then to default\
if user_zip.strip():
    filtered_df = df[df["Zip"] == user_zip.strip()]
elif dropdown_zip != "All":
    filtered_df = df[df["Zip"] == dropdown_zip]
else:
    filtered_df = df.copy()

# Only showed failed options if show failed only is selected
if fail_only:
    filtered_df = filtered_df[filtered_df["Passed"] == False]

# Create the map
map = folium.Map(location = [41.4831, -87.5320], zoom_start = 11)


st_data = st_folium(map)