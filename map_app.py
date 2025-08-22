import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# Set page config
st.set_page_config(page_title="Interactive Map App", layout="wide")

# Title
st.title("Interactive Map with Points of Interest")

# Sample data - you can replace this with your own data
locations = [
    {
        "name": "Eiffel Tower",
        "lat": 48.8584,
        "lon": 2.2945,
        "description": "Iconic iron lattice tower in Paris, France",
        "category": "Landmark",
        "year_built": 1889
    },
    {
        "name": "Statue of Liberty",
        "lat": 40.6892,
        "lon": -74.0445,
        "description": "Colossal neoclassical sculpture on Liberty Island",
        "category": "Monument",
        "year_built": 1886
    },
    {
        "name": "Big Ben",
        "lat": 51.5007,
        "lon": -0.1246,
        "description": "Famous clock tower in London, UK",
        "category": "Landmark",
        "year_built": 1859
    },
    {
        "name": "Sydney Opera House",
        "lat": -33.8568,
        "lon": 151.2153,
        "description": "Multi-venue performing arts centre in Sydney",
        "category": "Cultural Center",
        "year_built": 1973
    },
    {
        "name": "Colosseum",
        "lat": 41.8902,
        "lon": 12.4922,
        "description": "Ancient amphitheatre in Rome, Italy",
        "category": "Historical Site",
        "year_built": 80
    }
]

# Convert to DataFrame for easier handling
df = pd.DataFrame(locations)

# Sidebar for filtering
st.sidebar.header("Filter Options")
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=df["category"].unique(),
    default=df["category"].unique()
)

# Filter data based on selection
filtered_df = df[df["category"].isin(selected_categories)]

# Create the map
# Center the map on the mean of all coordinates
center_lat = filtered_df["lat"].mean()
center_lon = filtered_df["lon"].mean()

# Create a folium map
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=2,
    tiles="OpenStreetMap"
)

# Add markers to the map
for idx, row in filtered_df.iterrows():
    # Create popup HTML with styled content
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; width: 200px;">
        <h4 style="margin: 0 0 10px 0; color: #333;">{row['name']}</h4>
        <p style="margin: 5px 0; font-size: 14px;">
            <b>Category:</b> {row['category']}<br>
            <b>Year Built:</b> {row['year_built']}<br>
            <b>Description:</b> {row['description']}
        </p>
    </div>
    """
    
    # Add marker with popup
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row['name'],
        icon=folium.Icon(
            color='red' if row['category'] == 'Landmark' else
                  'blue' if row['category'] == 'Monument' else
                  'green' if row['category'] == 'Cultural Center' else
                  'purple' if row['category'] == 'Historical Site' else 'gray',
            icon='info-sign'
        )
    ).add_to(m)

# Display the map
col1, col2 = st.columns([3, 1])

with col1:
    # Render the map
    map_data = st_folium(m, width=700, height=500, returned_objects=["last_object_clicked"])

with col2:
    # Display information about clicked marker
    st.subheader("Point Information")
    
    if map_data['last_object_clicked'] and 'popup' in map_data['last_object_clicked']:
        st.info("Click information appears here after clicking a marker")
    else:
        st.info("Click on a marker to see details")

# Display data table below the map
st.subheader("All Locations")
st.dataframe(filtered_df[['name', 'category', 'year_built', 'description']], use_container_width=True)

# Statistics
# st.subheader("Statistics")
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.metric("Total Locations", len(filtered_df))
# with col2:
#     st.metric("Categories", len(filtered_df["category"].unique()))
# with col3:
#     oldest = filtered_df.loc[filtered_df["year_built"].idxmin()]
#     st.metric("Oldest Site", f"{oldest['name']} ({oldest['year_built']})")

# Instructions
with st.expander("How to use this app"):
    st.write("""
    1. **View the map**: The map shows all points of interest as markers
    2. **Click markers**: Click on any marker to see detailed information in a popup
    3. **Hover over markers**: Hover to see the name of the location
    4. **Filter by category**: Use the sidebar to filter locations by category
    5. **View data table**: Scroll down to see all location data in table format
    6. **Color coding**: 
       - Red: Landmarks
       - Blue: Monuments
       - Green: Cultural Centers
       - Purple: Historical Sites
    """)

# Footer
st.markdown("---")
