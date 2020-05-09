import plotly.express as px
from plotly.offline import plot
from gofor_problem_map.problem_map.models import District
import random
import pandas as pd
import geopandas as gpd
from django.core.serializers import serialize

def render_map():

    polies = serialize("geojson", District.objects.all(),
              geometry_field="poly")

    dummy_data = [random.randint(0,20) for k in range(District.objects.count())]
    df = gpd.GeoDataFrame(list(District.objects.all().values()))
    df["dummy"] = [random.randint(0,20) for k in range(District.objects.count())]
    fig = px.choropleth_mapbox(df, geojson=polies, locations='poly', color='dummy',
                               color_continuous_scale="Viridis",
                               range_color=(min(df.dummy), max(df.dummy)),
                               mapbox_style="carto-positron",
                               zoom=5, center = {"lat": 39.9108, "lon": 32.8601},
                               opacity=0.5,
                               labels={'name':'unemployment rate'}
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    # Put the figure in renderable component
    plot_div = plot(fig, output_type="div", include_plotlyjs=False, )
    return plot_div
