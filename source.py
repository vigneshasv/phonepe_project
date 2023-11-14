import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit as st
import os
from pprint import pprint
import pymysql
from sqlalchemy import create_engine



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
    i_states = json.load(open(r"D:\vs_code\phonepe\db\states_india.geojson"))
    df_trans = pd.read_csv(r"D:\vs_code\phonepe\db\agg-trans.csv")
    df_user = pd.read_csv(r"D:\vs_code\phonepe\db\agg-user.csv")
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
    fig = px.choropleth(qdf_trans, locations='id', geojson=i_states,hover_name="State",hover_data=['Transation_count'],color='Transation_amount',scope='asia')
    fig.update_geos(fitbounds="locations",visible=False)
    return(fig)




def Agg_Trans():
    path = r"D:\data\aggregated\transaction\country\india\state"
    Agg_state_list = os.listdir(path)
    sip = {
        "State": [],
        "Year": [],
        "Quater": [],
        "Transation_type": [],
        "Transation_count": [],
        "Transation_amount": [],
    }
    for i in Agg_state_list:
        v_i = path + "/" + i  # move upto states
        Agg_yr = os.listdir(v_i)
        for j in Agg_yr:
            v_j = v_i + "/" + j  # move upto years
            Agg_yr_list = os.listdir(v_j)
            for k in Agg_yr_list:
                v_k = v_j + "/" + k  # move upto quaterant
                Data = open(v_k, "r")
                D = json.load(Data)
                for z in D["data"]["transactionData"]:
                    Name = z["name"]
                    count = z["paymentInstruments"][0]["count"]
                    amount = z["paymentInstruments"][0]["amount"]
                    sip["Transation_type"].append(Name)
                    sip["Transation_count"].append(count)
                    sip["Transation_amount"].append(amount)
                    sip["State"].append(i)
                    sip["Year"].append(j)
                    sip["Quater"].append(int(k.strip(".json")))
    return(sip)


def Agg_User():
    path = r"D:\data\aggregated\user\country\india\state"
    Agg_state_list = os.listdir(path)
    Agg_state_list

    sip = {
        "State": [],
        "Year": [],
        "Quater": [],
        "Reg_user": [],
        "Device_brand": [],
        "Device_count": [],
    }
    for i in Agg_state_list:
        v_i = path + "/" + i
        Agg_yr = os.listdir(v_i)
        for j in Agg_yr:
            v_j = v_i + "/" + j
            Agg_yr_list = os.listdir(v_j)
            for k in Agg_yr_list:
                v_k = v_j + "/" + k
                Data = open(v_k, "r")
                D = json.load(Data)
                # if D['data']['usersByDevice'] is not None:
                try:
                    user = D["data"]["aggregated"]["registeredUsers"]
                    Brand = D["data"]["usersByDevice"][0]["brand"]
                    count = D["data"]["usersByDevice"][0]["count"]
                except:
                    pass
                sip["Reg_user"].append(user)
                sip["Device_brand"].append(Brand)
                sip["Device_count"].append(count)
                sip["State"].append(i)
                sip["Year"].append(j)
                sip["Quater"].append(int(k.strip(".json")))
    return(sip)            


def Map_Trans():
    path = r"D:\data\map\transaction\hover\country\india\state"
    Agg_state_list = os.listdir(path)
    Agg_state_list

    sip = {
        "State": [],
        "Year": [],
        "Quater": [],
        "District": [],
        "Transation_count": [],
        "Transation_amount": [],
    }
    for i in Agg_state_list:
        v_i = path + "/" + i
        Agg_yr = os.listdir(v_i)
        for j in Agg_yr:
            v_j = v_i + "/" + j
            Agg_yr_list = os.listdir(v_j)
            for k in Agg_yr_list:
                v_k = v_j + "/" + k
                Data = open(v_k, "r")
                D = json.load(Data)
                for z in D["data"]["hoverDataList"]:
                    Name = z["name"]
                    count = z["metric"][0]["count"]
                    amount = z["metric"][0]["amount"]
                    sip["District"].append(Name)
                    sip["Transation_count"].append(count)
                    sip["Transation_amount"].append(amount)
                    sip["State"].append(i)
                    sip["Year"].append(j)
                    sip["Quater"].append(int(k.strip(".json")))
    return(sip)                

    
def Map_User():
    path = r"D:\data\map\user\hover\country\india\state"
    Agg_state_list = os.listdir(path)

    sip = {
        "State": [],
        "Year": [],
        "Quater": [],
        "District": [],
        "reg_user": [],
        "app_opens": [],
    }
    for i in Agg_state_list:
        v_i = path + "/" + i
        Agg_yr = os.listdir(v_i)
        for j in Agg_yr:
            v_j = v_i + "/" + j
            Agg_yr_list = os.listdir(v_j)
            for k in Agg_yr_list:
                v_k = v_j + "/" + k
                Data = open(v_k, "r")
                D = json.load(Data)
                key = D["data"]["hoverData"]
                # pprint(list(key.keys()))
                for i in list(key.keys()):
                    name = i
                    user = key[i]["registeredUsers"]
                    appopen = key[i]["appOpens"]
                    sip["District"].append(name)
                    sip["reg_user"].append(user)
                    sip["app_opens"].append(appopen)
                    sip["State"].append(i)
                    sip["Year"].append(j)
                    sip["Quater"].append(int(k.strip(".json")))
    return(sip)



def Top_Trans():
    path = r"D:\data\top\transaction\country\india\state"
    Agg_state_list = os.listdir(path)
    Agg_state_list

    sip = {
        "State": [],
        "Year": [],
        "Quater": [],
        "Districts": [],
        "District_Transation_count": [],
        "District_Transation_amount": [],
    }
    for i in Agg_state_list:
        v_i = path + "/" + i
        Agg_yr = os.listdir(v_i)
        for j in Agg_yr:
            v_j = v_i + "/" + j
            Agg_yr_list = os.listdir(v_j)
            for k in Agg_yr_list:
                v_k = v_j + "/" + k
                Data = open(v_k, "r")
                D = json.load(Data)
                for z in D["data"]["districts"]:
                    Name = z["entityName"]
                    count = z["metric"]["count"]
                    amount = z["metric"]["amount"]
                sip["Districts"].append(Name)
                sip["District_Transation_count"].append(count)
                sip["District_Transation_amount"].append(amount)
                sip["State"].append(i)
                sip["Year"].append(j)
                sip["Quater"].append(int(k.strip(".json")))
    return(sip)



def Top_Trans_1():
    path = r"D:\data\top\transaction\country\india\state"
    Agg_state_list = os.listdir(path)
    Agg_state_list

    sip = {
        "State": [],
        "Year": [],
        "Quater": [],
        "pincodes": [],
        "Pincode_Transation_count": [],
        "Pincode_Transation_amount": [],
    }
    for i in Agg_state_list:
        v_i = path + "/" + i
        Agg_yr = os.listdir(v_i)
        for j in Agg_yr:
            v_j = v_i + "/" + j
            Agg_yr_list = os.listdir(v_j)
            for k in Agg_yr_list:
                v_k = v_j + "/" + k
                Data = open(v_k, "r")
                D = json.load(Data)

                for d in D["data"]["pincodes"]:
                    Name = d["entityName"]
                    count = d["metric"]["count"]
                    amount = d["metric"]["amount"]
                sip["pincodes"].append(Name)
                sip["Pincode_Transation_count"].append(count)
                sip["Pincode_Transation_amount"].append(amount)
                sip["State"].append(i)
                sip["Year"].append(j)
                sip["Quater"].append(int(k.strip(".json")))
    return(sip)

def Top_User():
    path = r"D:\data\top\user\country\india\state"
    Agg_state_list = os.listdir(path)
    Agg_state_list

    sip = {"State": [], "Year": [], "Quater": [], "Districts": [], "District_reg_user": []}
    for i in Agg_state_list:
        v_i = path + "/" + i
        Agg_yr = os.listdir(v_i)
        for j in Agg_yr:
            v_j = v_i + "/" + j
            Agg_yr_list = os.listdir(v_j)
            for k in Agg_yr_list:
                v_k = v_j + "/" + k
                Data = open(v_k, "r")
                D = json.load(Data)
                for z in D["data"]["districts"]:
                    name = z["name"]
                    user = z["registeredUsers"]
                    sip["Districts"].append(name)
                    sip["District_reg_user"].append(user)
                    sip["State"].append(i)
                    sip["Year"].append(j)
                    sip["Quater"].append(int(k.strip(".json")))
    return(sip)

def Top_User_1():
    path = r"D:\data\top\user\country\india\state"
    Agg_state_list = os.listdir(path)
    Agg_state_list

    sip = {"State": [], "Year": [], "pincode": [], "pincode_reg_user": [], "Quater": []}
    for i in Agg_state_list:
        v_i = path + "/" + i
        Agg_yr = os.listdir(v_i)
        for j in Agg_yr:
            v_j = v_i + "/" + j
            Agg_yr_list = os.listdir(v_j)
            for k in Agg_yr_list:
                v_k = v_j + "/" + k
                Data = open(v_k, "r")
                D = json.load(Data)
                for z in D["data"]["pincodes"]:
                    pin = z["name"]
                    reg = z["registeredUsers"]

                sip["pincode"].append(pin)
                sip["pincode_reg_user"].append(reg)
                sip["State"].append(i)
                sip["Year"].append(j)
                sip["Quater"].append(int(k.strip(".json")))
    return(sip)


d1 = pd.DataFrame(Agg_Trans())
d2 = pd.DataFrame(Agg_User())
d3 = pd.DataFrame(Map_Trans())
d4 = pd.DataFrame(Map_User())
d5 = pd.DataFrame(Top_Trans())
d6 = pd.DataFrame(Top_Trans_1())
d7 = pd.DataFrame(Top_User())
d8 = pd.DataFrame(Top_User())

# def start_sql():
mydb = pymysql.connect(
host="localhost",
user="root",
password="yoga1234$")
global cursor
cursor = mydb.cursor()
cursor.execute("CREATE DATABASE if not exists phonepe_pulse")
cursor.execute("USE phonepe_pulse")
engine = create_engine("mysql+pymysql://root:yoga1234$@localhost/phonepe_pulse")

d1.to_sql("agg_trans", engine, if_exists="append", index=False)
d2.to_sql("agg_user", engine, if_exists="append", index=False)
d3.to_sql("map_trans", engine, if_exists="append", index=False)
d4.to_sql("map_user", engine, if_exists="append", index=False)
d5.to_sql("top_trans", engine, if_exists="append", index=False)
d6.to_sql("top_trans_1", engine, if_exists="append", index=False)
d7.to_sql("top_user", engine, if_exists="append", index=False)
d8.to_sql("top_user_1", engine, if_exists="append", index=False)
    
    # return(d1,d2,d3,d4,d5,d6,d7,d8)


    
def query(input):
    
    
    match input:
        
        case "1. query top 10 states based on year and amount of transaction?":
            query1=("""SELECT distinct year, state, SUM(District_Transation_amount) AS top_transaction
            FROM Top_Trans
        -- WHERE year = ('2021')  -- Replace 'your_year' with the desired year
            GROUP BY year, state
            ORDER BY Top_Transaction DESC
            LIMIT 10;""")
            cursor.execute(query1)
            rows = cursor.fetchall()
            return pd.DataFrame(rows,columns=['Year','State','Top_Transaction'])

        case "2.query Top 10 states based on type and amount of transaction?":
            query2=(""" SELECT state,transation_type,sum(Transation_amount) AS total_trans_amount
            FROM Agg_Trans
            GROUP BY state,transation_type
            ORDER BY total_trans_amount DESC
            LIMIT 10;""")
            cursor.execute(query2)
            rows = cursor.fetchall()
            return pd.DataFrame(rows,columns=['State','Transaction_type',"total_trans_amount"])

    
        case "3. query Top 5 transacation_type based on transaction_amount?":
            query3=("""SELECT Transation_type,sum(Transation_amount) AS total_trans_amount
            FROM Agg_Trans
            GROUP BY  Transation_type
            ORDER BY   total_trans_amount DESC
            LIMIT 5;""")
            cursor.execute(query3)
            rows = cursor.fetchall()
            return pd.DataFrame(rows,columns=['Transaction_type','Total_Trans_Amount'])
        
                    
        case "4.query top 10 registered_user based on state and district?":
            query4=(""" SELECT a.state,a.Reg_user AS registered_user,d.Districts
            FROM Agg_User a
            JOIN Top_Trans d 
            ON a.state=d.state
            GROUP BY state,reg_user,Districts
            ORDER BY registered_user DESC
            LIMIT 10;""")
            cursor.execute(query4)
            rows = cursor.fetchall()
            return pd.DataFrame(rows,columns=['State','Registred_user','Districts'])

        case"5.query top 10 district based on states and count of transaction?":
            query5=("""SELECT state,Districts,District_Transation_count AS count_of_Transation
            FROM Top_Trans
            ORDER BY count_of_transation DESC;""")
            #group by state,District_Transation_count
            #limit 10
            cursor.execute(query5)
            rows = cursor.fetchall()
            return pd.DataFrame(rows,columns=['State',"Districts",'Count_of_Transaction'])

        case"6.query top 10 district based on state and amount of transaction?":
            query6=("""SELECT state,districts,sum(District_Transation_amount) AS amount_of_transaction
            FROM Top_Trans
            GROUP BY state,districts
            ORDER BY amount_of_transaction
            LIMIT 10;""")
            cursor.execute(query6)
            rows = cursor.fetchall()
            return pd.DataFrame(rows,columns=['State','District','Amount_of_Transaction'])

        case"7.query top 10 transaction_count based on district and states?":
            query7=("""SELECT Districts,state,sum(District_Transation_count) AS transaction_count
            FROM Top_Trans
            GROUP BY Districts,state
            ORDER BY   transaction_count DESC
            LIMIT 10;""")
            cursor.execute(query7)
            rows = cursor.fetchall()
            return pd.DataFrame(rows,columns=['District','State','Transaction_count'])

        case"8.query top 10 pincode_transaction_count dased on states and pincode?":
            query8=("""SELECT state,Pincodes,Pincode_Transation_count AS pincode_trans_count
            FROM Top_Trans_1
            ORDER BY pincode_trans_count desc
            LIMIT 10;""")
            cursor.execute(query8)
            rows = cursor.fetchall()
            return pd.DataFrame(rows,columns=['State','Pincodes','Pincode_Trans_count'])

        case"9.query top 10 register user based on pincode and year?":
            query9=("""SELECT year,Pincode,Pincode_reg_user AS Reg_User
            FROM Top_User_1
            -- group by year,pincode
            ORDER BY Reg_User desc
            LIMIT 10; """)
            cursor.execute(query9)
            rows = cursor.fetchaYll()
            return pd.DataFrame(rows,columns=['Year','Pincode','Reg_user'])
 
        case"10.query top 10 register user based on app_opens and states?":
            query10=("""SELECT state,app_opens,reg_user AS registered_user
            FROM Map_User
            ORDER BY registered_user DESC
            LIMIT 10;""")
            cursor.execute(query10)
            rows = cursor.fetchall()
            return pd.DataFrame(rows,columns=['State','app_opens','Registered_user'])
        
     
