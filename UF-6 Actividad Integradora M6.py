import streamlit as st
import numpy as np
import pandas as pd
import plotly as px

# import plotly.figure_factury as ff
# from brokeh.plotting import figure
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns

st.title("Police Incidents Reports from 2018 to 2020 in San Francisco")
df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")
# Modificación 1:
# Utilizamos el comando drop para eliminar las columnas no deseadas porque realmente sentia que no me podian aportar
# información relevante y solo hacia que cargara mas lento la información.
df = df.drop(
    [
        "Report Datetime",
        "Row ID",
        "Incident ID",
        "Incident Number",
        "CAD Number",
        "Report Type Code",
        "Report Type Description",
        "Filed Online",
        "Incident Code",
        "Intersection",
        "CNN",
        "Supervisor District",
        "point",
        "SF Find Neighborhoods",
        "Current Police Districts",
        "Current Supervisor Districts",
        "Analysis Neighborhoods",
        "HSOC Zones as of 2018-06-05",
        "OWED Public Spaces",
        "Central Market/Tenderloin Boundary Polygon - Updated",
        "Parks Alliance CPSI (27+TL sites)",
        "ESNCAG - Boundary File",
        "Areas of Vulnerability, 2016",
    ],
    axis=1,
)

#Modificación 2: Eliminamos las filas con valores nulos con drop.na
df = df.dropna(axis=0, how="any")

# st.dataframe(df)
st.markdown(
    "The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution."
)

mapa = pd.DataFrame()
mapa["Date"] = df["Incident Date"]
mapa["Day"] = df["Incident Day of Week"]
mapa["Police District"] = df["Police District"]
mapa["Neighborhood"] = df["Analysis Neighborhood"]
mapa["Incident Category"] = df["Incident Subcategory"]
mapa["Resolution"] = df["Resolution"]
mapa["lat"] = df["Latitude"]
mapa["lon"] = df["Longitude"]
mapa["Incident Year"] = pd.to_datetime(
    df["Incident Date"]
).dt.year  # Agregamos esta línea para incluir 'Incident Year'
mapa = mapa.dropna()
st.map(mapa.astype({"lat": "float32", "lon": "float32"}))

# Modificación 3: Quiero agregar mi nombre y la escuela
st.sidebar.markdown(
    "<h4 style='font-weight: bold; font-size: 12px; margin-bottom: 0; line-height: 1;'>Instituto Tecnológico de Monterrey</h4>\n\n<p style='font-size: 12px; margin-top: 0; line-height: 1;'>Made by:</p>\n\n<p style='font-weight: bold; font-size: 12px; margin-top: 0; line-height: 1;'>Christian Jesús Soto Vieyra Gil</p>\n\n<p style='font-size: 12px; margin-top: 0; line-height: 1;'>A01707759</p>",
    unsafe_allow_html=True,
)

# Modificación 4:
# Aqui voy a agregar un boton para seleccionar la información por año
subset_data3 = mapa
incident_year_input = st.sidebar.multiselect(
    "Incident Year", df["Incident Year"].unique().tolist()
)
if len(incident_year_input) > 0:
    subset_data3 = mapa[mapa["Incident Year"].isin(incident_year_input)]

subset_data2 = subset_data3
police_district_input = st.sidebar.multiselect(
    "Police District",
    mapa.groupby("Police District").count().reset_index()["Police District"].tolist(),
)
if len(police_district_input) > 0:
    subset_data2 = subset_data3[
        subset_data3["Police District"].isin(police_district_input)
    ]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
    "Neighborhood",
    subset_data2.groupby("Neighborhood").count().reset_index()["Neighborhood"].tolist(),
)
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2["Neighborhood"].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    "Incident Category",
    subset_data1.groupby("Incident Category")
    .count()
    .reset_index()["Incident Category"]
    .tolist(),
)
if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1["Incident Category"].isin(incident_input)]

# subset_data
# Modificacion 5: Todos los titulos de las graficas van a ir centrados y en negritas
st.markdown(
    "It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district."
)
st.markdown(
    '<h2 style="text-align: center; font-weight: bold;">Crime locations in San Francisco</h2>',
    unsafe_allow_html=True,
)
st.map(subset_data)
st.markdown(
    '<h2 style="text-align: center; font-weight: bold;">Crimes ocurred per day of the week</h2>',
    unsafe_allow_html=True,
)
st.bar_chart(subset_data["Day"].value_counts())
st.markdown(
    '<h2 style="text-align: center; font-weight: bold;">Crimes ocurred per date</h2>',
    unsafe_allow_html=True,
)
st.line_chart(subset_data["Date"].value_counts())
st.markdown(
    '<h2 style="text-align: center; font-weight: bold;">Type of crimes committed</h2>',
    unsafe_allow_html=True,
)
st.bar_chart(subset_data["Incident Category"].value_counts())

agree = st.button("Click to see Incident Subcategories")
if agree:
    st.markdown("Subtype of crimes committed")
    st.bar_chart(subset_data["Incident Subcategory"].value_counts())


# Modificación 6: Quise cambiar el formato de la grafica de pastel por una mas amigable a la vista y que se pueda comprender mejor
st.markdown(
    '<h2 style="text-align: center; font-weight: bold;">Resolution Status</h2>',
    unsafe_allow_html=True,
)  # Queria el grafico en negritas y centrado
# Obtener los valores y etiquetas para el gráfico de pastel
result = subset_data["Resolution"].value_counts()
labels = result.index
values = result.values
# Le puse una paleta colores de azules oscuros
colors = sns.color_palette("Blues_r", len(labels))
# Tambien queria que la parte mas grande del grafico fuera de rojo
max_index = values.argmax()
colors[max_index] = "red"

fig1 = go.Figure(
    data=[go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=colors))]
)
st.plotly_chart(fig1)
