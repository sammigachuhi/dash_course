from dash import Dash, html, dash_table, dcc, Input, Output, callback
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate

# The aim is to incorporate the shades table

# Incorporate the data
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/Dash-Course/makeup-shades/shades.csv")

# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Grid
grid = dag.AgGrid(
    id="grid",
    rowData=df.to_dict("records"),
    dashGridOptions={"pagination": True, "paginationAutoPageSize": True},
    columnSize="sizeToFit",
    columnDefs=[{"field": i} for i in df.columns],
)

# App layout
app.layout = html.Div([
    html.Div(children="The Shades Dataset"),
    # Create a dropdown that uses the column `Brand`, let `Revlon` be the initial value
    dcc.Dropdown(options=df["brand"].unique(), value="Revlon", multi=True, id="dropdown"),
    html.Div(id="dd-output-container"),
    # print(df["brand"].unique()),
    html.Hr(),
    # Insert radio items
    dcc.RadioItems(#options=df["group"].sort_values(ascending=True).unique(),
        options={
            0: "Fenty Beauty's PRO FILT'R Foundation Only",
            1: "Make Up For Ever's Ultra HD Foundation Only",
            2: "US Best Sellers",
            3: "BIPOC-recommended Brands with BIPOC Founders",
            4: "BIPOC-recommended Brands with White Founders",
            5: "Nigerian Best Sellers",
            6: "Japanese Best Sellers",
            7: "Indian Best Sellers"
        },
        value=7, inline=True,
        id="radioitem"),

    # Extra dropdowns
    html.Div(className="row", children=[
        html.Div(className="six columns", children=dcc.Dropdown(options=["H", "S", "V", "L"], value="H", id="dropdown1")),
        html.Div(className="six columns", children=dcc.Dropdown(options=["H", "S", "V", "L"], value="S", id="dropdown2"))
    ]),

    html.Hr(),

    # Select rows based on the dropdown and radio items
    html.Div(className="row", children=[
        html.Div(className="six columns", children=html.Div([grid])),
        html.Div(className="six columns", children=dcc.Graph(figure={}, id="scatterplot"))
    ]),

    # Insert a download button
    html.Button("Download CSV", id="btn_csv"),
    dcc.Download(id="download-dataframe")

])

# Callbacks
@callback(
    Output(component_id="dd-output-container", component_property="children"),
    Input(component_id="dropdown", component_property="value"),
    Input(component_id="radioitem", component_property="value"),
)
def update_output(dropdown, radioitem):
    return f"Selected brand name(s): {dropdown}\nSelected Group: {radioitem}"

@callback(
    Output(component_id="scatterplot", component_property="figure"),
    Input(component_id="dropdown1", component_property="value"),
    Input(component_id="dropdown2", component_property="value")
)
def update_graph(dropdown1, dropdown2):
    fig = px.scatter(df, x=dropdown1, y=dropdown2)
    return fig

# Callback for downloading dataframe
@callback(
    Output(component_id="download-dataframe", component_property="data"),
    Input(component_id="dropdown", component_property="value"),
    Input(component_id="btn_csv", component_property="n_clicks"),
    # prevent_initial_call=True
)
def func(dropdown, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return dcc.send_data_frame(df.to_csv, "selected_brands.csv")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
