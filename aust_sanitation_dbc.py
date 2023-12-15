# First load the necessary packages for your dash plotly app
from dash import Dash, dcc, html, callback, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import geopandas as gpd
import dash_ag_grid as dag
import plotly.express as px
import dash_leaflet as dl
import json

# Load the Dash bootstrap components
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template(["all"])

# Incorporate the Australian public toilets dataset
df = pd.read_csv("data/australia_toiletmap_csv.csv")
# df["StateName"] = ""

# The below if statement is borrowed from here: https://www.geeksforgeeks.org/create-a-new-column-in-pandas-dataframe-based-on-the-existing-columns/
def full_names(state):
    if state == "NSW":
        return "New South Wales"
    elif state == "QLD":
        return "Queensland"
    elif state == "SA":
        return "South Australia"
    elif state == "TAS":
        return "Tasmania"
    elif state == "VIC":
        return "Victoria"
    elif state == "WA":
        return "Western Australia"
    elif state == "ACT":
        return "Australian Capital Territory"
    else:
        return "Northern Territory"

df["StateName"] = df["State"].map(full_names)

# Insert our `StateName` column to index 5
# See here: https://stackoverflow.com/questions/13148429/how-to-change-the-order-of-dataframe-columns
df.insert(5, "StateName", df.pop("StateName"))

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# App layout
app.layout = dbc.Container([
    # Heading
    html.H2(children="Public Toilets in Australia"),
    # Introduce the dropdown, show only states
    dcc.Dropdown(options=df["StateName"].unique(),
                 value="Western Australia",
                 multi=True,
                 placeholder="Select a State...",
                 id="state_dropdown"),

    # Some space
    html.Hr(),

    # A html for printing out selected State, at least for now
    html.Div(id="statement"),

    # Some space please
    html.Hr(),
    html.Hr(),

    # Insert a map
    dcc.Graph(figure={}, id="map"),

    # Some space
    html.Hr(),

    # Show table, at least temporarily for now
    html.Div(
        # children=[grid],
        id="table"),

    # Some space
    html.Hr(),

    # Show a download button for downloading selected states
    html.Div(children=[
        dbc.Button("Download CSV", id="btn_csv", color="dark", className="me-1"),
        dcc.Download(id="download-dataframe-csv")
    ]),

])

# Create callback for State dropdown
@callback(
    Output(component_id="statement", component_property="children"),
    Input(component_id="state_dropdown", component_property="value")
)
def update_state(selected_state):
    res = str(selected_state)[1:-1]
    return f"You have selected {res} State(s)"

# Callback to update GeoJSON layer based on selected state
@app.callback(
    Output(component_id="map", component_property="figure"),
    Input(component_id="state_dropdown", component_property="value")
)
def update_map(selected_state):
    states = []
    for i in selected_state:
        states.append(i)
    dff = df.loc[df["StateName"].isin(states)]

    fig = px.scatter_mapbox(dff, lat="Latitude", lon="Longitude", hover_name="Name", color="StateName",
                            hover_data=["Town", "StateName", "Address1"],
                            zoom=3, height=500,
                            labels={
                                "StateName": "State"
                            })

    fig.update_layout(mapbox_style="open-street-map",
                      mapbox_bounds={"west": 100, "east": 180, "south": -80, "north": -10},
                      margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      )

    fig.update_traces(marker_size=5)
    # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

# Create callback for reactive dash-ag-grid table
@callback(
    Output(component_id="table", component_property="children"),
    Input(component_id="state_dropdown", component_property="value")
)
def update_grid(selected_state):
    # res = str(selected_state)[1:-1]
    states = []
    for i in selected_state:
        states.append(i)
    dff = df.loc[df["StateName"].isin(states)]
    grid = dag.AgGrid(
        id="australia_public_toilets",
        className="ag-theme-alpine-dark",
        rowData=dff.to_dict("records"),
        columnDefs=[{"field": i} for i in df.columns],
        dashGridOptions={"pagination": True},
    )
    return grid

# Callback to download selected states dataframe
@callback(
    Output(component_id="download-dataframe-csv", component_property="data"),
    Input(component_id="btn_csv", component_property="n_clicks"),
    State(component_id="state_dropdown", component_property="value"),
    prevent_initial_call=True
)
def func_clicks(n_clicks, selected_state):
    states = []
    for i in selected_state:
        states.append(i)

    dff = df.loc[df["StateName"].isin(states)]

    return dcc.send_data_frame(dff.to_csv, "toilets.csv")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)








































