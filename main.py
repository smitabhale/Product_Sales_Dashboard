import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Sales Dashboard',
                   page_icon=':bar_chart:',
                   layout='wide'
)
@st.cache
def get_data_from_excel():
    df =pd.read_excel(
    io="C:\\smita-software enginner material\\Dashboards using python\\Project1-supermarket\\supermarkt_sales.xlsx",
    engine='openpyxl',
    sheet_name='Sales',
    skiprows=3,
    usecols='B:R',
    nrows=1000,
)
# add hour column to data frame
    df['Hour']=pd.to_datetime(df['Time'], format="%H:%M:%S").dt.hour
    return df
df=get_data_from_excel()



# --------------------------sidebar---------------
st.sidebar.header("Please Filter Here:")
city=st.sidebar.multiselect(
    'Select the city:',
    options=df['City'].unique(),
    default=df['City'].unique()
)

customer_type=st.sidebar.multiselect(
    "Select the customer: ",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()

)

gender=st.sidebar.multiselect(
    'Select the gender:',
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)
# st.dataframe(df)
df_selection=df.query(
    "City == @city & Customer_type == @customer_type & Gender ==@gender"
)
# st.dataframe(df_selection)
# print(type(df_selection))

#-------------MAINPAGE------------
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(), 1)
star_rating= ":star:" * int(round(average_rating, 0))
average_sales_by_trasaction = round(df_selection["Total"].mean(),2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales}")
with middle_column:
    st.subheader("Average Rating")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average sales per transcation")
    st.subheader(f"US $ {average_sales_by_trasaction}")

st.markdown("---")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line=(
df_selection.groupby(by=["Product line"])["Total"].sum().sort_values()
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by product Line</b>",
    color_discrete_sequence=["#0083b8"] * len(sales_by_product_line),
    template="plotly_white",
)


# SALES BY HOUR
sales_by_hour=(
df_selection.groupby(by=["Hour"])["Total"].sum().sort_values()
)

fig_hourly_sales = px.bar(
    sales_by_hour,
    x="Total",
    y=sales_by_hour.index,
    orientation="h",
    title="<b>Sales by Hour</b>",
    color_discrete_sequence=["#0083b8"] * len(sales_by_hour),
    template="plotly_white",
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width =True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

