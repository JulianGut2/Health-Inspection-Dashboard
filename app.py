# General imports
import streamlit as st
import pandas as pd
from collections import Counter
import folium 
from streamlit_folium import st_folium

# Adding this to fix speed bug, looping through all those inspections points renders the streamlit app very slow
from folium.plugins import MarkerCluster

# Create a header to introduce our users 
st.title("Chicago Food Inspection Map")

df = pd.read_csv("data/clean_food_inspections.csv")

# Ensuring that all of the zips in our data frame are stored as strings not integers
df['Zip'] = df['Zip'].astype(str).str.strip()

# Create a non null, unique, list of zip code options
zip_options = df["Zip"].dropna().unique().tolist()

# Create a subheader to direct user input
st.sidebar.subheader("Zip Code Filter")

# Creating a hybrid
user_zip = st.sidebar.text_input("Enter a Zip Code (optional):")
dropdown_zip = st.sidebar.selectbox("Or select one:", ["All"] + zip_options)

# Add an option to only view failed health inspection results
fail_only = st.sidebar.checkbox("Show only failed inspections", value = False)

# Use Caching here so streamlit wont have to rerun the map logic every single time
# therefore increasing the speed of the program
@st.cache_data
def get_filtered_data(df, user_zip, dropdown_zip, fail_only):
    # Filtering logic
    if user_zip.strip():
        filtered = df[df["Zip"] == user_zip.strip()]
    elif dropdown_zip != "All":
        filtered = df[df["Zip"] == dropdown_zip]
    else:
        filtered = df.copy()

    # Faily only filter
    if fail_only:
        filtered = filtered[filtered["Passed"] == False]

    return filtered

filtered_df = get_filtered_data(df, user_zip, dropdown_zip, fail_only)

if filtered_df.empty:
    st.warning("No results were found for your selection")

# Spinner when generating map for a better UX
with st.spinner("Generating map..."):
# Create the map
    map = folium.Map(location = [41.8781, -87.6298], zoom_start = 11, tiles = "CartoDB positron")

# This will serve to increase the speed of our program by creating a layer of clusters.
    marker_cluster = MarkerCluster().add_to(map)

# Now we should proceed with adding points into the map
    for _, row in filtered_df.iterrows():
        result = "Pass" if row["Passed"] else "Fail"
        tooltip = f"{row['DBA Name']}<br>{result}<br>{row['Inspection Date'][:10]}"
        color = "green" if row["Passed"] else "red"

        folium.CircleMarker(
            location = [row["Latitude"], row['Longitude']],
            radius = 4,
            color = color,
            fill = True,
            fill_opacity = 0.7,
            popup = tooltip
        ).add_to(marker_cluster)

    st_data = st_folium(map, width = 900, height = 600)

st_data