import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit as st

pio.renderers.default = 'firefox'
new = {'telangana': 0,
        'andaman-&-nicobar_trans-islands': 35,
        'andhra-pradesh': 28, 
        'arunachal-pradesh': 12, 
        'assam': 18, 
        'bihar': 10,
        'chhattisgarh': 22,
        'dadra-&-nagar-haveli-&-daman-&-diu': 25, 
        'goa': 30, 
        'gujarat': 24, 
        'haryana': 6, 
        'himachal-pradesh': 2, 
        'jammu-&-kashmir': 1, 
        'jharkhand': 20, 
        'karnataka': 29, 
        'kerala': 32, 
        'lakshadweep': 31, 
        'madhya-pradesh': 23, 
        'maharashtra': 27, 
        'manipur': 14, 
        'chandigarh': 4, 
        'puducherry': 34, 
        'punjab': 3, 
        'rajasthan': 8, 
        'sikkim': 11, 
        'tamil-nadu': 33, 
        'tripura': 16, 
        'uttar-pradesh': 9, 
        'uttarakhand': 5, 
        'west-bengal': 19, 
        'odisha': 21, 
        'ladakh': 26, 
        'meghalaya': 17, 
        'mizoram': 15, 
        'nagaland': 13, 
        'delhi': 7}



def import_files():
    global i_states, df_trans, df_user
    i_states = json.load(open("/home/suresh/windows_share/phonepe/db/states_india.geojson", 'r'))
    df_trans = pd.read_csv("/home/suresh/windows_share/phonepe/db/agg-trans.csv")
    df_user = pd.read_csv("/home/suresh/windows_share/phonepe/db/agg-user.csv")
    df_trans.loc[:, 'id'] = df_trans['State'].map(new)
    for feature in i_states["features"]:
        feature['id'] = feature['properties']['state_code']
    return df_trans

def get_dataframe_map(year, quater, typ_e):
    query = 'Year == Y_ and Quater == Q_ and Transation_type == "T_"'
    query = query.replace("Y_", year)
    query = query.replace("Q_", quater)
    query = query.replace("T_", typ_e)
    global qdf_trans
    qdf_trans = df_trans.query(query)

def show_map():
    fig = px.choropleth(qdf_trans, locations='id', geojson=i_states, color='Transation_amount',scope='asia')
    fig.update_geos(fitbounds="locations",visible=False)
    return(fig)

def total_amount():
    return int(df_trans["Transation_amount"].sum())

def send_data_request(year, quater, state, type):
    global Year, Quater, State, Transation_type
    Year = year
    Quater = quater
    State = state
    Transation_type = type

def get_data_frame():
    return df_trans.query("Year == @Year & Quater == @Quater & State == @State & Transation_type == @Transation_type ")

def bar_update_trans():
    global bar_trans
    bar_trans=(get_data_frame().groupby(by=["Year"]).sum()[["Transation_count"]].sort_values(by="Transation_count"))

def bar_update_user():
    global bar_user
    bar_user=(df_user.groupby(by=["Year"]).sum()[["Reg_user"]].sort_values(by="Reg_user"))

def bar_chart_agg_trans():
    

    fig_image=px.bar(bar_trans,
        x="Transation_count",
        y=bar_trans.index,
        orientation="h",
        title="<b> Transation in Phonepe Based on Years </b>",
        color_discrete_sequence=["#0083b8"] * len(bar_trans),
        template="plotly_white",
    )
    fig_image.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        title_font_size= 26,
        yaxis=(dict(tickmode="linear"))
    )
    return fig_image

def pie_chart_agg_trans():

    fig_image=px.pie(bar_trans,
                    values="Transation_count",
                    names=bar_trans.index,
                    title="<b> Transation in Phonepe </b>",
    )
    fig_image.update_layout(
        title_font_size= 26
    )
    fig_image.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    return fig_image

def bar_chart_agg_user():
    fig_image=px.bar(bar_user,
        x="Reg_user",
        y=bar_user.index,
        orientation="h",
        title="<b>Registred user in Phonepe Based on Year</b>",
        color_discrete_sequence=["#0083b8"] * len(bar_user),
        template="plotly_white",
    )
    fig_image.update_layout(
        title_font_size= 26,
    )
    return fig_image

def pie_chart_agg_user():
        
    fig_image=px.pie(bar_user,
                    values="Reg_user",
                    names=bar_user.index,
                    title="<b> Transation in Phonepe </b>",
    )
    fig_image.update_layout(
        title_font_size= 26,
    )
    fig_image.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )
    return fig_image




     
