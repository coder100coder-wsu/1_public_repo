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
    # dcc.RadioItems(
    #     id='state_name',
    #     options=[{'value': x, 'label': x}
    #              for x in df['state_name'].str.upper().unique()
    #              ],
    #     value=df['state_name'].str.upper()[0],
    #     labelStyle={'display': 'inline-block'}
    # ),

    dcc.Dropdown(
        id="selected_dropdown",
        options=[{"label": x, "value": x} for x in df_merged['state_name'].str.upper().unique()],
        value="ca",  # df_merged['state_name'][0],
        clearable=False,
        multi=False
    ),

    dcc.Graph(id="choropleth"),
    #dcc.Graph(id="choropleth_2"),
])


@app.callback(
    Output("choropleth", "figure"),
    [Input("selected_dropdown", "value")])
def display_choropleth(selected_dropdown):
    df_sal = pd.DataFrame(df.groupby(by=['state_name'], axis=0, level=None,
                                            group_keys=True, observed=False, as_index=True,
                                            sort=False, dropna=True)
                          .median()
                          .reset_index(inplace=False, drop=False)
                          )

    fig_map = px.choropleth(
        df,
        locationmode="USA-states",
        locations=df[df['state_name'] == selected_dropdown]['state_name'].str.upper().unique(),
        labels={'sal_min_yearly': 'sal_min_yearly column'},
        # median value for given column, from df_sal above
        color=df_sal[df_sal['state_name'] == selected_dropdown]['sal_min_yearly'],
        range_color=(int(df['sal_min_yearly'].min()),  # global min
                     int(df['sal_max_yearly'].max())  # global max
                     )
        # range_color = (0, df[df['state_name'] == selected_dropdown]['sal_min_yearly'].max())
    )
    fig_map.update_geos(fitbounds="locations", scope="usa",
                        visible=False, showcountries=True, countrycolor="Black",
                        showsubunits=True, subunitcolor="Blue"
                        )
    fig_map.update_layout(height=300, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig_map


# @app.callback(
#     Output("choropleth_2", "figure"),
#     [Input("selected_dropdown", "value")])
# def display_choropleth_2(selected_dropdown):
#     df_sal = pd.DataFrame(df_merged.groupby(by=['state_name'], axis=0, level=None,
#                                             group_keys=True, observed=False, as_index=True,
#                                             sort=False, dropna=True)
#                           .median()
#                           .reset_index(inplace=False, drop=False)
#                           )
#
#     fig_map_2 = px.choropleth(
#         df,
#         locationmode="USA-states",
#         locations=df[df['state_name'] == selected_dropdown]['state_name'].str.upper().unique(),
#         labels={'sal_min_yearly': 'sal_min_yearly column'},
#         color=df_sal[df_sal['state_name'] == selected_dropdown]['sal_min_yearly'],
#         range_color=(df[df['state_name'] == selected_dropdown]['sal_min_yearly'].min(),# local min
#                      df[df['state_name'] == selected_dropdown]['sal_max_yearly'].max())# local max
#         # DOES NOT WORK HERE # color_continuous_scale="Viridis", DOES NOT WORK HERE
#         # DOES NOT WORK HERE # range_color=(0, 12),
#     )
#     fig_map_2.update_geos(fitbounds="locations", scope="usa",
#                           visible=False, showcountries=True, countrycolor="Black",
#                           showsubunits=True, subunitcolor="Blue"
#                           )
#     fig_map_2.update_layout(height=200, margin={"r": 0, "t": 0, "l": 0, "b": 0})
#
#     return fig_map_2


if __name__ == "__main__":
    app.run_server(debug=False)
