from dash import Dash, html, dash_table, dcc, Input, Output, callback
import pandas as pd

# The aim is to incorporate the shades table

# Incorporate the data
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/Dash-Course/makeup-shades/shades.csv")

# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

options={
            0: "Fenty Beauty's PRO FILT'R Foundation Only",
            1: "Make Up For Ever's Ultra HD Foundation Only",
            2: "US Best Sellers",
            3: "BIPOC-recommended Brands with BIPOC Founders",
            4: "BIPOC-recommended Brands with White Founders",
            5: "Nigerian Best Sellers",
            6: "Japanese Best Sellers",
            7: "Indian Best Sellers"
        }

# App layout
app.layout = html.Div([
    html.Div(children="The Shades Dataset"),
    # Create a dropdown that uses the column `Brand`, let `Revlon` be the initial value
    dcc.Dropdown(options=df["brand"].unique(), value="Revlon", multi=True, id="dropdown"),
    html.Div(id="dd-output-container"),
    # print(df["brand"].unique()),
    html.Hr(),
    # Insert radio items
    dcc.RadioItems(
        options=[v for v in options.values()],
        value=7, inline=True,
        id="radioitem"),
    # Select rows based on the dropdown and radio items
    dash_table.DataTable(data=df.to_dict("records"), page_size=15, id="table"),
])

# Callbacks
@callback(
    Output(component_id="dd-output-container", component_property="children"),
    Input(component_id="dropdown", component_property="value"),
    Input(component_id="radioitem", component_property="value"),
)
def update_output(dropdown, radioitem):
    return f"Selected brand name(s): {dropdown}\nSelected radioitem {radioitem}"

# Run the app
if __name__ == "__main__":
    app.run(debug=True)



















