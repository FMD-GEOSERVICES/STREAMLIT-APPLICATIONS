import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import streamlit_folium as sf
from streamlit_folium import st_folium

#Page configuration
st.set_page_config(
    page_title="Population Dashboard",
    page_icon="D:\\Users\\ALIENWARE\\Downloads\\FMD_OLD_LOGO.jpg",
    layout="wide"
)

#Web App Title
# st.title("Welcome to the World's Population Dashboard")
st.markdown (
   """<div style="text-align: center; 
   font-size: 40px; color: Gold; 
   font-family: 'Elephant'">
        Welcome to the World's Population Dashboard
    </div>""",
    unsafe_allow_html=True,
)
#Credit 
st.markdown(
    """<div style="text-align: center;">
        <i>(Created by FMD GEO-SERVICES🌍)</i>
    </div>
    """, unsafe_allow_html=True
)

#Fetching world population data from File directory
@st.cache_data
def get_data():
    csv_file_path = f"D:\\Users\\ALIENWARE\\Downloads\\World_Population_Data.csv"
    geojson_path = f"D:\\Users\\ALIENWARE\\Downloads\\World countries and states.geojson"
    try:
           df = pd.read_csv(csv_file_path, encoding="ISO-8859-1")
           gdf = gpd.read_file(geojson_path)
           return df, gdf
    except Exception as e:
            return None, None
population_data, geodata = get_data()

    # The condition below will display the population dataframe
    # if population_data is not None:
    #     st.dataframe(population_data)
    # else:
    #     st.write("Fetching data...")

# Text widgets
st.text("Please choose a country to explore its population data and geographical information:")
# if population_data is not None and geodata is not None:


# Dropdown menu for selecting a country
    # df = population_data
country_list = population_data["Country/Territory"].unique()
selected_country = st.selectbox(
"Select a country",
["Type country's name here"] + list(country_list)
)

# Creating two columns
col1, col2 = st.columns([1, 1])

if selected_country is not None and selected_country != "Type country's name here":

# Filtering data for the selected country
    country_data = population_data[population_data["Country/Territory"] == selected_country].iloc[0]
    
# Column 1: Country Statistics
    with col1:
        st.subheader("Country's Statistics")
        st.write(f"**Country:** {country_data['Country/Territory']}")
        st.write(f"**Continent:** {country_data['Continent']}")
        st.write(f"**Capital:** {country_data['Capital']}")
        st.write(f"**Area:** {country_data['Area (km²)']} km²")
        st.write(f"**Population:** {country_data['World Population Percentage']:.2f}%")
        st.write(f"**Density:** {country_data['Density (per km²)']} per km²")
else:
    st.warning("Please select a country from the dropdown list to proceed.")


with col2:
    st.subheader("Population by year")
    available_years = [
            "2022 Population", "2020 Population",
            "2015 Population", "2010 Population",
            "2000 Population", "1990 Population","1980 Population", "1970 Population"
        ]
    selected_years = st.multiselect(
            "Select year to view population data:",
            available_years
        )

# Calling the selected Country's map in Column 1
with col1:
# Selected Country's map
    st.subheader("Country Map")
map = folium.Map()
if selected_country is not None and selected_country != "Type country's name here":
    selected_geometry = geodata[geodata['admin'] == selected_country]
    folium.GeoJson(data = selected_geometry).add_to(map)

selected_geometry = geodata[geodata['admin'] == selected_country]
if not selected_geometry.empty:
        if selected_geometry.geometry.notnull().any():
                
# Initializing Folium map centered on the selected country
                country_coords = selected_geometry.geometry.centroid.iloc[0].coords[0]
                country_map = folium.Map(
                      location=[country_coords[1],
                                country_coords[0]],
                                zoom_start=5.5,
                    )
        with col1:
# Add selected country to the map
                folium.GeoJson(
                    data = selected_geometry,
                    name = "Selected Country",
                    style_function=lambda x:{
                        "fillColor": "orange",
                        "color": "blue",
                        "weight": 2,
                        "fillOpacity": 0.01,
                    },
                    tooltip=folium.GeoJsonTooltip(
                        fields=["admin"],
                        aliases=["Country Name:"],
                        localize=True,
                    ),
                    ).add_to(country_map)
                bounds = selected_geometry.total_bounds
                country_map.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
                st_folium(country_map)
else:
        st.warning(f"**Geometry** data for {"Country"} is invalid or missing.", icon="⚠️")
        
# Show population data for selected years
with col2:
    if selected_years is not None and selected_country != "Type country's name here":
        population_data = {year: country_data[year] for year in selected_years}

        with col2:
# Bar Chart
            chart_data = pd.DataFrame({
            "Year": [year.split(" ")[0] for year in selected_years],
            "Population": list(population_data.values())
        })

# Display the bar chart
        # I can also use st.write for a subheader i the same manner with markdown using ###
        # st.write("### Population Over Selected Years")
        # or
        st.subheader("Population Over Selected Years")
        st.bar_chart(
              chart_data.set_index("Year"),
              color = "#FFD700"
            )