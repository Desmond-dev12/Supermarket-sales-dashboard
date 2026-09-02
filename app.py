import streamlit as st
import pandas as pd 
import plotly.express as px

# page config = page title
st.set_page_config(page_title='Supermarket Sales Dashboard', layout='wide')

st.markdown("""
<style>
    .header {background-color: #2C3E50;
    color: #FFFFFF;streamlit
    padding: 15px;
    border-radius: 10px;
    text-align: center;
        }
</style>
<div class="header">
     <h1>Super Market Sales Dashboard</h1>
     </div>
     """, unsafe_allow_html=True)


@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path,encoding="latin1")
    data.columns = data.columns.str.lower().str.strip().str.replace(" ","_")
    data["date"] = pd.to_datetime(data["date"],errors="coerce")
   
    data["day_of_week"]= data["date"].dt.day_name()
    
    
    return data

data_path = "supermarket_sales.csv" 
data = load_data(data_path)


st.sidebar.header("Filters")
selected_branch = st.sidebar.multiselect(
    "select Branch", options= data["branch"].unique(),default=data["branch"].unique()
)

selected_product = st.sidebar.multiselect(
    "select Product line", options= data["product_line"].unique(),default=data["product_line"].unique()
)


selected_customer = st.sidebar.multiselect(
    "select Customer_type", options= data["customer_type"].unique(),default=data["customer_type"].unique()
)

min_date = data["date"].min().date()
max_date = data["date"].max().date()
  
selected_date = st.sidebar.date_input(
    "selected date range",
    value = (min_date, max_date),
    min_value= min_date,
    max_value= max_date
)
if not selected_date or len(selected_date) !=2:
    st.warning("Please select a valid date range")
    st.stop()


filtered_data = data[(data["branch"].isin(
selected_branch))&


(data["product_line"].isin(
selected_product))&


(data["customer_type"].isin(
selected_customer))&


(data["date"] >= pd.to_datetime(selected_date[0]))&


(data["date"] <= pd.to_datetime(selected_date[1]))
]
            

if filtered_data.empty:
    st.warning("No Data found for the filters")
    st.stop()

st.dataframe(filtered_data.head())


filtered_data["total"] = filtered_data["total"].round(2)
filtered_data["gross_income"] = filtered_data["gross_income"].round(2)
filtered_data["rating"] = filtered_data["rating"].round(2)
filtered_data["quantity"] = filtered_data["quantity"].round(2)

total_sales = filtered_data["total"].sum()
gross_income = filtered_data["gross_income"].sum()
total_quantity = filtered_data["quantity"].sum()
avg_rating = filtered_data["rating"].mean()


st.subheader("Key Metrics")
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.metric(label="Total_Sales", value=f"${total_sales:,.2f}")

with col2:
    st.metric(label="Gross Income", value=f"${gross_income:,.2f}")

with col3:
    st.metric(label="Total Quantity", value=f"{total_quantity:,.0f}")

with col4:
    st.metric(label="Average Rating", value=f"{avg_rating:,.1f}")



sales_by_branch = filtered_data.groupby("branch")["total"].sum().reset_index()
sales_by_branch["total"] = sales_by_branch["total"].round(1)
st.subheader("Total Sales by Branch")
fig_branch = px.bar(
    sales_by_branch,
    title="Total Sales by Branch",
    x="branch",
    y="total",
    text="total",
    color="branch"
)
st.plotly_chart(fig_branch,use_container_width=True)



sales_by_product = filtered_data.groupby("product_line")["total"].sum().reset_index()
avg_rating_by_product = filtered_data.groupby("product_line")["rating"].mean().reset_index()

sales_by_product["total"] = sales_by_product["total"].round(1)

avg_rating_by_product["rating"] = avg_rating_by_product["rating"].round(2)

st.subheader("Total Sales and Rating by Product Line")
col1,col2 = st.columns(2)
with col1:
    fig_product_sales = px.bar(
        sales_by_product, x="product_line",
                          y="total",
                orientation="v",
                     title="sales by product line",
                     text="total",
 color_discrete_sequence=px.colors.sequential.Plasma 
    )
    fig_product_sales.update_layout(showlegend=False, height=500)
    fig_product_sales.update_layout(xaxis=dict(tickangle=-60),
     margin=dict(b=100, t=40,))

    st.plotly_chart(fig_product_sales, use_container_width=True)
    with col2:
     fig_product_rating = px.bar(
            avg_rating_by_product, x="product_line",
                                   y="rating",
                         title="Average Rating by Product Line",
                         text="rating",
                         color="product_line", 
                         
                             
         color_discrete_sequence=px.colors.sequential.Viridis

     )
    fig_product_rating.update_layout(showlegend=False, height=500)
    fig_product_rating.update_layout(xaxis=dict(tickangle=-45),
     margin=dict(b=100, t=40,))
    

    st.plotly_chart(fig_product_rating, use_container_width=True)


    sales_by_customer = filtered_data.groupby("customer_type")["total"].sum().reset_index()
    sales_by_payment = filtered_data.groupby("payment")["total"].sum().reset_index()
    sales_trend = filtered_data.groupby("date")["total"].sum().reset_index()



fig_sales_by_customer = px.pie(
                               sales_by_customer, names="customer_type",
                               values="total",
                              title="Sales Distribution by Customer Type",
                              color="customer_type",
                              hole=0.4,
                              color_discrete_sequence=px.colors.sequential.Teal

                            
    )
st.plotly_chart(fig_sales_by_customer, use_container_width=True)

fig_payment_sales = px.pie(sales_by_payment,
                           names="payment",
                           values="total",
                           title="Sales Distribution by Payment Method",
                           color="payment",
                           hole=0.4,
                           color_discrete_sequence=px.colors.sequential.Plasma)

st.plotly_chart(fig_payment_sales, use_container_width=True)

fig_sales_trend = px.line(sales_trend,
                         x="date",
                         y="total",
                         title="Daily Sales Trend",
                         markers=True,
                         color_discrete_sequence=["#2C3E50"]
                          )

st.plotly_chart(fig_sales_trend, use_container_width=True)


data["date"]=pd.to_datetime(data["date"], errors="coerce")
data["date"]= data["date"].ffill()
sales_by_day = data.groupby("day_of_week")["total"].sum().reset_index()
sales_by_day["day_of_week"] = sales_by_day["day_of_week"].round(2)


day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
sales_by_day = pd.Categorical(sales_by_day["day_of_week"],
                              categories=day_order,
                              ordered=True)

st.divider()
st.header("Executive Summary and Business Insights")
st.subheader("Click to view Executive Summary")
with st.expander("Executive Summary & Business Insights"):
    st.markdown(""" ### **Business Insights**
    * **Balanced Branch Performance**: Revenue accross A, B, C is remarkably uniform ranging between 106k and 110.5k,
     indicating consistent regional demand without reliance on single standout store.
    * **Category Revenue vs Satisfaction Divergence:** Food and beverages generates the highest
     sales revenue (56.1k), yet Health and Beauty earns the highest customer rating (7.11), while Sports
      and Travel scores lowest in customer satisfaction (6.82).
    * **Even Customer Segmentation:** Sales are split almost evenly between Members (50.8%), and Normal non-members(49.2%),
    showing strong casual foot traffic but potential underutilization of the loyalty program.
    * **Balanced Payment Ecosystem & Volatile Trends:** Payment methods are evenly distributed among E-wallet (34.7%), Cash (34.1%), 
    and Credit Card (31.2%), through daily sales trends fluctuate heavily with sharp peaks reaching 7,000+.


    ### **Strategic Recommmendations**
    * **Optimize Product Inventory Allocation:** Increase stock and shelf space for high- revenue like Food and Beverages while auditing
    supplier qualiity for underperforming product lines like Sports and Travel.
    
    * **Enhance Loyalty Program Value:** introduce targeted member-only perks or points multipliers to incentivize the 49.2% non-member 
    baseline into joining the loyalty program.
    * **Leverage Payment Channel Promotion:** Partner with popular E-wallet providers to run promotional cashback campaigns, reducing 
    cash-handling costs and boosting digital checkout speed.

    * **Capitalize on Peak Sales Cycles:** Analyze time-of-day and day-of-week data behind the daily revenue spikes(near the 7,000 threshold)
    to optimize shift staffing and dynamic promotional messaging.
    
    

    """)


