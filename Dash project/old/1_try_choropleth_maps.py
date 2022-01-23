import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import json
import dash
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as po

df_test = pd.read_csv("D:\\13_USA education\\wayne state\\0_WSU coursework\\DS_E_6k\\final "
                      "project\\test_csv.csv")
df_merged = df_test.copy()
df_merged = df_merged.dropna()
# ['title', 'company', 'sal_min_yearly', 'sal_max_yearly', 'city_name', 'state_name']
# print("old info \n", df_merged.info(), "\n")
df_merged['sal_max_yearly'] = df_merged['sal_max_yearly'].astype(int)
df_merged['sal_min_yearly'] = df_merged['sal_min_yearly'].astype(int)

# df = px.data.election()
# geojson = px.data.election_geojson()
# candidates = df.winner.unique()

df = df_merged

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("map:"),
    dcc.RadioItems(
        id='state_name',
        options=[{'value': x, 'label': x}
                 for x in df['state_name'].str.upper().unique()
                 ],
        value=df['state_name'].str.upper()[0],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="choropleth"),
])


@app.callback(
    Output("choropleth", "figure"),
    [Input("state_name", "value")])
def display_choropleth(state_name):
    fig_map = px.choropleth(
        df,
        locationmode="USA-states",
        locations=df['state_name'].str.upper().unique(),
        # color= df.groupby(by='state_name')['sal_min_yearly']
        # range_color=(0, df['sal_min_yearly'].max()),
    )
    fig_map.update_geos(fitbounds="locations", scope="usa",
                        visible=False, showcountries=True, countrycolor="Black",
                        showsubunits=True, subunitcolor="Blue"
                        )
    fig_map.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig_map


if __name__ == "__main__":
    app.run_server(debug=False)
