from install_pkgs import import_or_install

required_pkgs = {'pandas', 'dash', 'plotly.express', 'plotly.graph_objects'}
for pkg in required_pkgs:
    import_or_install(pkg)

import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

# read csv file
df_test = pd.read_csv("use_for_plot_data.csv")
# create copy, so that original data is not modified
df_merged = df_test.copy()
# drop null values
df_merged = df_merged.dropna()
# ['title', 'company', 'sal_min_yearly', 'sal_max_yearly', 'city_name', 'state_name']
# print("old info \n", df_merged.info(), "\n")

# recast to datatype int
df_merged['sal_max_yearly'] = df_merged['sal_max_yearly'].astype(int)
df_merged['sal_min_yearly'] = df_merged['sal_min_yearly'].astype(int)

# rename to generic var name
# df = px.data.tips()
df = df_merged

app = dash.Dash(__name__)

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
#                 meta_tags=[{'name': 'viewport',
#                             'content': 'width=device-width, initial-scale=1.0'}]
#                 )


app.layout = html.Div([
    # specify title for part/section of dashboard
    html.P("Minimum Salary Distribution"),
    # display bunch of radio buttons
    # radio button means select-only-one
    dcc.RadioItems(
        id='title',
        # get radio buttons from data
        options=[{'value': x, 'label': x}
                 for x in df_merged['title'].unique()],
        # specify default value selected from available radio items
        value="data_scientist",
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="box-plot"),

    html.P("salary_slider"),
    dcc.RangeSlider(
        id='slider_sal_min',
        min=df_merged['sal_min_yearly'].min(),
        max=df_merged['sal_min_yearly'].max(),
        step=20000,
        marks={0: 'min', 600000: 'max'},
        value=[10000, 200000]
    ),
    dcc.Graph(id="scatter-plot"),

    dcc.Dropdown(
        id="selected_dropdown",
        options=[{"label": x, "value": x} for x in df_merged['state_name']],
        value="il",  # df_merged['state_name'][0],
        clearable=False,
        multi=False
    ),
    dcc.Graph(id="bar-chart"),

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
    Output("box-plot", "figure"),
    Input("title", "value")
)
def generate_chart(x):  # , y):
    # print("x= ", x)#, "y= ", y)
    fig_box = px.box(df, x=df_merged.loc[df_merged["title"] == x, 'sal_min_yearly'])  # ,
    return fig_box


@app.callback(
    Output("scatter-plot", "figure"),
    Input("slider_sal_min", "value")
)
def update_bar_chart(slider_range):
    low, high = slider_range
    df_plot_this = df_merged[df_merged['sal_min_yearly'] > low]
    df_plot_this = df_plot_this[df_plot_this['sal_min_yearly'] < high]
    fig_scatter = px.scatter(
        df_plot_this, x="sal_max_yearly", y="title",
        color="state_name", size='sal_max_yearly',
        hover_data=['sal_min_yearly'])
    return fig_scatter


@app.callback(
    Output("bar-chart", "figure"),
    [Input("selected_dropdown", "value")])
def update_bar_chart(selected_item_in_dropdown):
    mask = df_merged["state_name"] == selected_item_in_dropdown
    df_plot_this = df_merged[mask]
    df_plot_this = df_plot_this.sort_values(by='sal_max_yearly', ascending=False)
    df_plot_this = df_plot_this.reset_index(drop=True)
    # print(df_plot_this.loc[:,('state_name','sal_max_yearly','title')])
    fig_bar = px.bar(df_plot_this,
                     x="title", y="sal_max_yearly",
                     color="sal_max_yearly",
                     title="salary by title for selected state",
                     # labels={"sal_max":"sal_max_yearly"}
                     barmode="group", facet_col="company"
                     )
    return fig_bar


@app.callback(
    Output("choropleth", "figure"),
    [Input("state_name", "value")])
def display_choropleth(state_name):
    fig_map = fig = px.choropleth(
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
    # app.run_server(debug=True)