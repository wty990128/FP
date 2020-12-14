"""
CS230:      Section HB1
Name:       Frank Wang
Data:       Streamlit, Numpy, Pandas, Plotly
Description:
This program creates a map which shows the magnitude of earthquake by heatmap,
a bar chart states the count of earthquakes by date and a scatter chart shows
the relation between magnitude and depth of the event.

I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
URL:        Link to your web application online (see extra credit)
"""
import streamlit as st
import numpy as np
import pandas as pd
import pydeck
import plotly.express as px

DATA_URL = 'earthquakes_us_20201123.csv'

MAP_BOX_KEY = 'pk.eyJ1IjoiYWRtaW5hZG1pbmFkbWluMTIzNDUiLCJhIjoiY2tpa2RsdDVlMDh3ODMzanoyenVmcDY2bCJ9.AYrXcKLJauGhIS3Jwx7FPw'
MAP_STYLE = 'mapbox://styles/mapbox/light-v9'

COLUMN_NAME = {
    'DATE_COLUMN': 'time',
    'MAG_COLUMN': 'mag',
    'DEPTH_COLUMN': 'depth',
    'MAGTYPE_COLUMN': 'magtype',
}


def load_data():
    data = pd.read_csv(DATA_URL)
    data.rename(lambda x: str(x).lower(), axis='columns', inplace=True)
    data[COLUMN_NAME['DATE_COLUMN']] = pd.to_datetime(data[COLUMN_NAME['DATE_COLUMN']])
    return data


def create_map(stream_it, data, view_state):
    """
    creates a map which shows the magnitude of earthquake by heatmap
    :return:
    """
    geojson = pydeck.Layer(
        'HeatmapLayer',
        data[['latitude', 'longitude', COLUMN_NAME['MAG_COLUMN']]],
        opacity=0.9,
        get_position=["longitude", "latitude"],
        get_weight=COLUMN_NAME['MAG_COLUMN']
    )

    stream_it.pydeck_chart(pydeck.Deck(
        layers=[geojson],
        initial_view_state=view_state,
        map_style=MAP_STYLE,
        mapbox_key=MAP_BOX_KEY,
    ))


def create_earthquake_count_fig(data):
    """
    create a bar chart stat the count of earthquakes by date
    :param data:
    :return:
    """
    magtype_data = data.loc[:, [COLUMN_NAME['DATE_COLUMN'], COLUMN_NAME['MAGTYPE_COLUMN']]]
    magtype_data.loc[:, COLUMN_NAME['DATE_COLUMN']] = magtype_data[COLUMN_NAME['DATE_COLUMN']].dt.floor('d').dt.date
    # use Pandas to group and count different magtype in every day
    stat_by_magtype = magtype_data.groupby([COLUMN_NAME['DATE_COLUMN'], COLUMN_NAME['MAGTYPE_COLUMN']],
                                           as_index=False).size().sort_values(COLUMN_NAME['DATE_COLUMN'])
    fig = px.bar(stat_by_magtype, x=COLUMN_NAME['DATE_COLUMN'], y='size', color=COLUMN_NAME['MAGTYPE_COLUMN'],
                 title="Earthquake count grouped by date",
                 opacity=0.8)
    fig.update_layout(xaxis_tickangle=-90)
    return fig


def create_earthquake_depth_fig(data):
    """
    create a scatter chart shows the relation between magnitude and depth of the event
    :param data:
    :return:
    """
    depth_data = data.loc[:, [COLUMN_NAME['MAG_COLUMN'], COLUMN_NAME['DEPTH_COLUMN']]]
    return px.scatter(depth_data, x=COLUMN_NAME['MAG_COLUMN'], y=COLUMN_NAME['DEPTH_COLUMN'],
                      color=COLUMN_NAME['MAG_COLUMN'])


def main():
    st.title('Final Project – Building a Data-Driven Python Application')
    st.subheader('Earthquakes in US')
    data_load_state = st.text('Loading data...')
    data = load_data()
    data_load_state.text("Done! (using st.cache)")

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    st.subheader('Map of earthquakes')
    view_state = pydeck.ViewState(
        longitude=-120,
        latitude=40,
        zoom=2,)
    create_map(st, data, view_state)

    st.subheader('Earthquake count')
    st.plotly_chart(create_earthquake_count_fig(data))

    st.subheader('Earthquake depth')
    st.plotly_chart(create_earthquake_depth_fig(data))


if __name__ == '__main__':
    main()
