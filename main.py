
from source import *
import streamlit as st


df = import_files()

st.set_page_config(page_title="Phonepe Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
)

st.sidebar.header("Filter Data:")
with st.sidebar:
    st.title("data filter")
    m_year = st.selectbox("year",("2018", "2019", "2020", "2021", "2022"))
    m_quater = st.selectbox("quater",("1", "2", "3", "4"))
    m_type_ = st.selectbox("type",("Recharge & bill payments", "Peer-to-peer payments", "Merchant payments", "Financial Services", "Others"))

    year = st.sidebar.multiselect(
        "select the Year:",
        options=df["Year"].unique(),
        default=df["Year"].unique()
    )

    quater =st.sidebar.multiselect(
        "select the Quater:",
        options=df["Quater"].unique(),
        default=df["Quater"].unique()
        
    )

    state=st.sidebar.multiselect(
        "select the state:",
        options=df["State"].unique(),
        default=df["State"].unique()
    )

    transation_type=st.sidebar.multiselect(
        "select the type:",
        options=df["Transation_type"].unique(),
        default=df["Transation_type"].unique()
        
    )

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")
st.subheader("Total_amount:")
st.subheader(f"{total_amount():,}")

send_data_request(year, quater, state, transation_type)
st.dataframe(get_data_frame())

bar_update_trans()
bar_update_user()
left_column,right_column = st.columns(2)
left_column.plotly_chart(bar_chart_agg_trans(),use_container_width=True)
right_column.plotly_chart(pie_chart_agg_trans())

left_column,right_column = st.columns(2)
left_column.plotly_chart(bar_chart_agg_user(),use_container_width=True)
right_column.plotly_chart(pie_chart_agg_user(),use_container_width=True)



get_dataframe_map(m_year, m_quater, m_type_)
plot = show_map()
st.plotly_chart(plot)

st.sidebar.header("Top 10 filtered data:")
with st.sidebar:
    add_selectbox = st.selectbox(
    "Select mode",
    ("Get data", "Query")
    )
    
    if add_selectbox is "Get data":
       
        gu = st.button("get data", type="primary")
        
    if add_selectbox is "Query":
            select_query = st.selectbox(
        "Select your Query?",
        ("1. query top 10 states based on year and amount of transaction?",
         "2.query Top 10 states based on type and amount of transaction?",
         "3. query Top 5 transacation_type based on transaction_amount?",
         "4.query top 10 registered_user based on state and district?",
         "5.query top 10 district based on states and count of transaction?",
         "6.query top 10 district based on state and amount of transaction?",
         "7.query top 10 transaction_count based on district and states?",
         "8.query top 10 pincode_transaction_count dased on states and pincode?",
         "9.query top 10 register user based on pincode and year?",
         "10.query top 10 register user based on app_opens and states?")
         )
        
    qu = st.button("get query..", type="primary")
    
if add_selectbox is "Get data" and gu:
    st.write('Data getting....') 
    #start_sql() 
    st.write('Data loaded')         
 
elif add_selectbox is "Query" and qu:
    st.title('Loading Query') 
    df = query(select_query)
    st.title('loaded') 
    st.dataframe(df)

