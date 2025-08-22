import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Interactive Map of Uppsala art", 
    layout="wide",
    initial_sidebar_state="auto"
)

# Title
st.title("Interactive Map of Uppsala art")

locations = [
    {
        "name": "Point 1",
        "lat": 59.85811918766938,
        "lon": 17.630661164758212,
        "description": "Location point 1",
        "category": "Point",
        "year_built": 2024
    },
    {
        "name": "Point 2",
        "lat": 59.857276979539556,
        "lon": 17.63114768262532,
        "description": "Location point 2",
        "category": "Point",
        "year_built": 2024
    },
    {
        "name": "Point 3",
        "lat": 59.85817704850423,
        "lon": 17.63354186274294,
        "description": "Location point 3",
        "category": "Point",
        "year_built": 2024
    },
    {
        "name": "Point 4",
        "lat": 59.856968378847384,
        "lon": 17.628932746107186,
        "description": "Location point 4",
        "category": "Point",
        "year_built": 2024
    },
    {
        "name": "Point 5",
        "lat": 59.855547492942534,
        "lon": 17.63127571373036,
        "description": "Location point 5",
        "category": "Point",
        "year_built": 2024
    },
    {
        "name": "Point 6",
        "lat": 59.85626115815376,
        "lon": 17.633567468946474,
        "description": "Location point 6",
        "category": "Point",
        "year_built": 2024
    },
    {
        "name": "Point 7",
        "lat": 59.85845992229671,
        "lon": 17.638855150514736,
        "description": "Location point 7",
        "category": "Point",
        "year_built": 2024
    }
]

# Convert to DataFrame for easier handling
df = pd.DataFrame(locations)

# Sidebar for filtering
st.sidebar.header("🎯 Filter Options")
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=df["category"].unique(),
    default=df["category"].unique()
)

# Add mobile-friendly layout option
st.sidebar.markdown("---")
st.sidebar.header("📱 Display Options")

# Filter data based on selection
filtered_df = df[df["category"].isin(selected_categories)]

# Create the map
# Center the map on the mean of all coordinates
center_lat = filtered_df["lat"].mean()
center_lon = filtered_df["lon"].mean()

# Create a folium map
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=15,
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
# Use responsive layout that stacks on mobile
if st.sidebar.checkbox("Show point information sidebar", value=False):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Render the map with responsive sizing
        map_data = st_folium(m, width=None, height=500, returned_objects=["last_object_clicked"])
    
    with col2:
        # Display information about clicked marker
        st.subheader("Point Information")
        
        if map_data['last_object_clicked'] and 'popup' in map_data['last_object_clicked']:
            st.info("Click information appears here after clicking a marker")
        else:
            st.info("Click on a marker to see details")
else:
    # Full width map for mobile-friendly experience
    map_data = st_folium(m, width=None, height=500, returned_objects=["last_object_clicked"])
    
    # Point information below map for mobile
    if map_data['last_object_clicked'] and 'popup' in map_data['last_object_clicked']:
        st.info("✅ Marker clicked - see popup for details")
    else:
        st.info("📍 Click on a marker to see details")

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
