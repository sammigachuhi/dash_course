# Load packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate the data
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/Dash-Course/US-Exports/2011_us_ag_exports.csv")

# Initialize the App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div([
    # Insert title
    html.Div(children="US Agricultural Exports", id="my-title"),
    # Insert dropdown
    dcc.Dropdown(options=df["state"].unique(), value="Alabama", multi=True, id="state-dropdown"),
    html.Div(id="dd-output-container"),
    html.Hr(),
    # Add an empty dcc Graph
    dcc.Graph(figure={}, id="graph1"),
    dash_table.DataTable(data=df.to_dict("records"),
                         columns=[{"name": i, "id": i} for i in df.columns],
                         filter_action="native",
                         filter_options={"placeholder_text": "Filter column..."},
                         sort_action="native",
                         sort_mode="multi",
                         page_size=10)
])

# Callback for dropdown
@callback(
    Output(component_id="dd-output-container", component_property="children"),
    Input(component_id="state-dropdown", component_property="value")
)
def dropdown(value):
    return f"You have selected the following states: {value}"

# Callback for dataframe
@callback(
    Output(component_id="graph1", component_property="figure"),
    Input(component_id="state-dropdown", component_property="value")
)
def select_states(state_selected):
    states = []
    for i in state_selected:
        states.append(i)
    df_country = df.loc[df["state"].isin(states)]
    fig = px.bar(df_country, x="state", y=['beef','pork','fruits fresh'],
                 labels={"state": "US State"})

    # Change some layouts
    fig.update_layout(
        yaxis_title="Value of Exports",
        legend_title="Agricultural Products",
        transition_duration=10
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)






















