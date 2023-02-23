#HeatMap
from folium.plugins import HeatMap
import folium
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
#donut
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.backends.backend_agg import RendererAgg
import altair as alt
# set page layout
st.set_page_config(
    page_title="LLS2LINE Exploration",
    page_icon="🗾",
    #layout="wide",
    initial_sidebar_state="expanded",
)
st.title("🌍 🗾 LLS2LINE Exploration")

def explore(df):


    df_types = pd.DataFrame(df)
    from datetime import datetime

    min_ts = datetime.strptime(min(df["Date"]), "%d/%m/%Y %H:%M:%S.%f")
    max_ts = datetime.strptime(max(df["Date"]), "%d/%m/%Y %H:%M:%S.%f")
    df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y %H:%M:%S.%f")
    #print(min_ts,max_ts)
    st.sidebar.subheader("Inputs")
    min_selection, max_selection = st.sidebar.slider("Timeline", min_value=min_ts, max_value=max_ts, value=[min_ts, max_ts])
    # Filter Data based on selection
    st.write(f"Filtering between {min_selection.date()} & {max_selection.date()}")
    df = df[(df["Date"] >= min_selection) & (df["Date"] <= max_selection)]
    st.write(f"Data Points: {len(df)}")
    # DATA
    st.write('แสดงข้อมูลไฟล์ที่อัพโหลด')
    st.write(df)
    # SUMMARY


    st.write('กราฟแท่งแสดงจำนวนทั้งหมด')
    chart = df_types['Line'].unique()
    chart = df['Line']
    result = {}
    # we write for loop and if-else
    # to check every item in the animals list
    for TS in chart:
        if TS in result:
            result[TS] += 1
        else:
            result[TS] = 1
    # print output
    # Create DataFrame from dict
    ts_df = pd.DataFrame(result.items(), columns=["name", "marks"])
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:

    labels=ts_df["name"].iloc[1:]
    sizes=ts_df["marks"].iloc[1:]
    labels=labels.values.tolist()
    sizes=sizes.values.tolist()
    #print(labels,sizes)
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    #fig1, ax1 = plt.subplots()
    #ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    #ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #st.pyplot(fig1)

    data = {
        'labels': labels,
        'sizes': sizes
    }

    df = pd.DataFrame(data)
    #st.dataframe(df)
    
    c = alt.Chart(df).mark_bar().encode(x='sizes', y='labels', color='labels',tooltip=[
                alt.Tooltip("sizes", title="จำนวนครั้ง"),
                alt.Tooltip("labels", title="ชื่อสายส่ง"),
            ])
    st.altair_chart(c, use_container_width=True)
    



def transform(df):
    # Select sample size
    df['lat'] = df['Latitude']
    df['lon'] = df['Longtitude']
    #print(df)
    #st.map(df)
    from datetime import datetime
    # data.csv has columns ['date_time', 'value']
    # Example:
    #   date_time,value
    #   2015-05-15 10:05:03,95.93390214
    #   2015-05-15 10:05:43,81.03359351
    #   2015-05-15 10:05:47,71.66595487
    #   2015-05-15 10:05:12,76.99855579
    #       :
    #       :  
    # Calculate the timerange for the slider
    #df['Date'] = pd.to_datetime(df['Date'])
    min_ts = datetime.strptime(min(df["Date"]), "%d/%m/%Y %H:%M:%S.%f")
    max_ts = datetime.strptime(max(df["Date"]), "%d/%m/%Y %H:%M:%S.%f")
    df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y %H:%M:%S.%f")
    #print(min_ts,max_ts)
    st.sidebar.subheader("Inputs2")
    min_selection, max_selection = st.sidebar.slider("Timeline", min_value=min_ts, max_value=max_ts, value=[min_ts, max_ts])
    #print(min_selection,max_selection)
    #print(df["Date"])
    
    #st.sidebar.subheader("Inputs")
    #df['Date'] = pd.to_datetime(df['Date'])
    #start_dt = st.sidebar.date_input('Start date', value=df['Date'].min())
    #end_dt = st.sidebar.date_input('End date', value=df['Date'].max())
    #if start_dt <= end_dt:
    #    df = df[df['Date'] > datetime(start_dt.year, start_dt.month, start_dt.day)]
    #    df = df[df['Date'] < datetime(end_dt.year, end_dt.month, end_dt.day)]
    #    st.write(df)
    #    st.map(df)
    #else:
    #    st.error('Start date must be > End date')

    # Filter Data based on selection
    st.write(f"Filtering between {min_selection.date()} & {max_selection.date()}")
    df = df[(df["Date"] >= min_selection) & (df["Date"] <= max_selection)]
    st.write(f"Data Points: {len(df)}")
    # Plot the GPS coordinates on the map
    st.map(df)


    # Toggles for the feature selection in sidebar
    show_heatmap = st.sidebar.checkbox("Show Heatmap")
    show_ScatterplotLayer = st.sidebar.checkbox("Show ScatterplotLayers")
    show_histograms = st.sidebar.checkbox("Show Histograms")

    if show_heatmap:
        # Plot the heatmap using folium. It is resource intensive!
        # Set the map to center around Munich, Germany (48.1351, 11.5820)
        map_heatmap = folium.Map(location=[18.534, 103.611], zoom_start=7)

        # Filter the DF for columns, then remove NaNs
        heat_df = df[["lat", "lon"]]
        heat_df = heat_df.dropna(axis=0, subset=["lat", "lon"])

        # List comprehension to make list of lists
        heat_data = [
            [row["lat"], row["lon"]] for index, row in heat_df.iterrows()
        ]

        # Plot it on the map
        HeatMap(heat_data).add_to(map_heatmap)

        # Display the map using the community component
        st.subheader("Heatmap")
        folium_static(map_heatmap)



    if show_ScatterplotLayer:

        st.write('แสดง ScatterplotLayer ของพื้นที่ทั้งหมด')
        import pydeck as pdk
        chart_data = df[["lon", "lat","Line","Date"]]
        #print(chart_data['lon'])
        tooltip = {
            "html":
                "<b>Name:</b> {Line} <br/>"
                '<b>Elevation Value:<br/> {elevationValue}',
            "style": {
                "backgroundColor": "steelblue",
                "color": "black",
            }
        }

        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=18.534, 
                longitude=103.611,
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                type='HexagonLayer',
                data=chart_data,
                get_position=["lon", "lat"],
                radius=300,
                height="medprice",
                get_line_color=[0, 0, 0],
                elevation_scale=30,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                
                ),
                pdk.Layer(
                    type='ScatterplotLayer',
                    data=chart_data,
                    get_position=["lon", "lat"],
                    get_color=[200, 30, 0, 160],
                    get_radius=300,
                    get_line_color=[0, 0, 0],
                    pickable=True,
                    onClick=True,
                    filled=True,
                    line_width_min_pixels=10,
                ),
                pdk.Layer(
                type="TextLayer",
                data=chart_data,
                pickable=False,
                get_position=["lon", "lat"],
                get_text="Line",
                get_size=100,
                sizeUnits='meters',
                get_color=[0, 0, 0],
                get_angle=0,
                # Note that string constants in pydeck are explicitly passed as strings
                # This distinguishes them from columns in a data set
                getTextAnchor= '"middle"',
                get_alignment_baseline='"bottom"',
    )],tooltip=tooltip
            
        ))


        options = st.multiselect(
            'กรุณาเลือกพื้นที่ เพื่อให้แสดงบน ScatterplotLayer',df['Line'].unique())
        st.write('แสดงข้อมูลเฉพาะที่เลือก:', df[df['Line'].isin(options)])
        # If the user selects one or more colors:
        if options:
            # Set the flag to indicate the color select has been changed
            import pydeck as pdk

            chart_data = df[["lon", "lat","Line","Date"]]
            condition_1 = chart_data['Line'].isin(options)
            g1=chart_data[condition_1]
            #print(chart_data['lon'])
            tooltip = {
                "html":
                    "<b>Name:</b> {Line} <br/>"
                    '<b>Elevation Value:<br/> {elevationValue}',
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "black",
                }
            }

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=18.534, 
                    longitude=103.611,
                    zoom=11,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                    type='HexagonLayer',
                    data=g1,
                    get_position=["lon", "lat"],
                    radius=300,
                    height="medprice",
                    get_line_color=[0, 0, 0],
                    elevation_scale=30,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                    
                    ),
                    pdk.Layer(
                        type='ScatterplotLayer',
                        data=g1,
                        get_position=["lon", "lat"],
                        get_color=[200, 30, 0, 160],
                        get_radius=300,
                        get_line_color=[0, 0, 0],
                        pickable=True,
                        onClick=True,
                        filled=True,
                        line_width_min_pixels=10,
                    ),
                    pdk.Layer(
                    type="TextLayer",
                    data=g1,
                    pickable=False,
                    get_position=["lon", "lat"],
                    get_text="Line",
                    get_size=100,
                    sizeUnits='meters',
                    get_color=[0, 0, 0],
                    get_angle=0,
                    # Note that string constants in pydeck are explicitly passed as strings
                    # This distinguishes them from columns in a data set
                    getTextAnchor= '"middle"',
                    get_alignment_baseline='"bottom"',
        ),],tooltip=tooltip
                
            ))




    if show_histograms:
        # Plot the histograms based on the dates of data points
        years = df.groupby(df["Date"].dt.year).count().plot(kind="bar")
        years.set_xlabel("Year of Data Points")
        hist_years = years.get_figure()
        st.subheader("Data Split by Year")
        st.pyplot(hist_years)

        days = df.groupby(df["Date"].dt.day).count().plot(kind="bar")
        days.set_xlabel("Month of Data Points")
        hist_days = days.get_figure()
        st.subheader("Data Split by days")
        st.pyplot(hist_days)

        hours = df.groupby(df["Date"].dt.hour).count().plot(kind="bar")
        hours.set_xlabel("Hour of Data Points")
        hist_hours = hours.get_figure()
        st.subheader("Data Split by Hours of Day")
        st.pyplot(hist_hours)

    return df
def get_df(file):
  # get extension and read file
    extension = file.name.split('.')[1]
    if extension.upper() == 'CSV':
        df = pd.read_csv(file)
    elif extension.upper() == 'XLSX':
        df = pd.read_excel(file, engine='openpyxl')
    elif extension.upper() == 'PICKLE':
        df = pd.read_pickle(file)
    #print(df)
    return df
def main():
    Select1 = st.checkbox('นำเข้าไฟล์')
    Select2 = st.checkbox('ไฟล์ปัจจุบัน')
    if Select1:
        st.title('กรุณานำเข้าฐานข้อมูล')
        st.write('โปรแกรมสำหรับวิเคราะห์ข้อมูล LLs2line')
        file = st.file_uploader("อัพโหลดไฟล์", type=['csv' ,'xlsx','pickle'])
        if not file:
            st.write("รองรับไฟล์ .csv หรือ .xlsx ")
            return
        df = get_df(file)
        #df = transform(df)
        #explore(df)
        task = st.sidebar.radio('การทำงาน', ['ข้อมูล', 'แผนภาพ'], 0)
        if task == 'ข้อมูล':
            df=explore(df)
        elif task == "แผนภาพ":
            df=transform(df)
    if Select2:
        df = pd.read_csv("LLS2LINE_08August_2022.csv")
        task = st.sidebar.radio('การทำงาน', ['ข้อมูล', 'แผนภาพ'], 0)
        if task == 'ข้อมูล':
            df=explore(df)
        elif task == "แผนภาพ":
            df=transform(df)
main()
