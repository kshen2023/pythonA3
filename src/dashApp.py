import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.express as px

# Fetch the data from the Winnipeg Open Data Portal
url = "https://data.winnipeg.ca/resource/hfwk-jp4h.json"
response = requests.get(url)
data = response.json()

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)


df['coordinates'] = df['point'].apply(lambda x: x.get('coordinates') if x else None)
df['longitude'] = df['coordinates'].apply(lambda x: x[0] if x else None)
df['latitude'] = df['coordinates'].apply(lambda x: x[1] if x else None)

# Drop the complex columns
df.drop(columns=['location', 'point', 'coordinates'], inplace=True)

# Initialize the Dash app with Bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the Dash app
app.layout = html.Div([
    html.H1("City of Winnipeg Tree Data"),
    html.H2("Tree Data Table"),
    dash_table.DataTable(
        id='tree-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
    ),
    html.H2("Tree Location Scatter"),
    dcc.Graph(
        id='tree-scatter-plot',
        figure=px.scatter(
            df,
            x="longitude",
            y="latitude",
            color="common_name",
            hover_data=['tree_id', 'common_name', 'neighbourhood'],
            labels={'longitude': 'Longitude', 'latitude': 'Latitude'},
            title='Tree Locations in Winnipeg'
        )
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
