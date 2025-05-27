import streamlit as st
from streamlit_option_menu import option_menu
import pymysql
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import openpyxl



# Function to load the data
@st.cache_data
def load_data():
    # Change the path as needed, or use a relative path for deployment
    file_path = "E:\\Course\\Aamir\\Ola\\OLA PROJECT\\OLA_DataSet.xlsx"
    data = pd.read_excel(file_path)
    return data





# Function to plot the rides per day distribution
def plot_rides_per_day_distribution(data):
    data['Date'] = pd.to_datetime(data['Date'])  
    rides_per_day = data['Date'].value_counts().sort_index()

    fig = px.line(
        x=rides_per_day.index,
        y=rides_per_day.values,
        labels={'x': 'Date', 'y': 'Number of Rides'},
        title="Rides Per Day"
    )
    st.plotly_chart(fig)


# Booking Status Distribution (Pie Chart)
def plot_booking_status_pie_chart(data):
    status_counts = data['Booking_Status'].value_counts()
    
    fig = px.pie(
        names=status_counts.index,
        values=status_counts.values,
        title='Distribution of Booking Status',
        hole=0.3
    )
    
    st.plotly_chart(fig)


# Bookings by Day of Week (Line Plot)
def plot_bookings_by_day(data):
    data['day_of_week'] = data['Date'].dt.day_name()

    day_counts = data['day_of_week'].value_counts().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])

    fig = px.line(
        x=day_counts.index,
        y=day_counts.values,
        labels={'x': 'Day of Week', 'y': 'Number of Bookings'},
        title='Bookings by Day of Week',
        markers=True
    )

    st.plotly_chart(fig)


# Payment Method Distribution (Pie Chart)
def plot_payment_method_pie_chart(data):
    payment_counts = data['Payment_Method'].value_counts()

    fig = px.pie(
        names=payment_counts.index,
        values=payment_counts.values,
        title='Distribution of Payment Methods',
        hole=0.3
    )
    
    st.plotly_chart(fig)


# Distribution of Ratings (Customer vs Driver)
def plot_ratings_distribution(data):
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=data['Customer_Rating'],
        name='Customer Ratings',
        nbinsx=20,
        opacity=0.6,
        marker=dict(color='blue')
    ))

    fig.add_trace(go.Histogram(
        x=data['Driver_Ratings'],
        name='Driver Ratings',
        nbinsx=20,
        opacity=0.6,
        marker=dict(color='red')
    ))

    fig.update_layout(
        title='Customer vs Driver Ratings Distribution',
        barmode='overlay',
        xaxis_title='Rating',
        yaxis_title='Count',
        bargap=0.2
    )

    st.plotly_chart(fig)


# Reasons for Incomplete Rides (Bar Plot)
def plot_incomplete_rides_reasons(data):
    reason_counts = data['Incomplete_Rides_Reason'].value_counts()

    fig = px.bar(
        x=reason_counts.index,
        y=reason_counts.values,
        labels={'x': 'Reasons', 'y': 'Count'},
        title='Incomplete Rides Reasons'
    )

    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)


# Incomplete Rides Distribution (Pie Chart)
def plot_incomplete_rides_pie_chart(data):
    incomplete_counts = data['Incomplete_Rides'].value_counts()

    fig = px.pie(
        names=incomplete_counts.index,
        values=incomplete_counts.values,
        title='Incomplete Rides Distribution',
        color=incomplete_counts.index,
        color_discrete_map={'1': 'lightblue', '0': 'salmon'}
    )

    st.plotly_chart(fig)


# Distribution of Ride Distance
def plot_ride_distance_distribution(data):
    fig = px.histogram(
        data, 
        x='Ride_Distance', 
        nbins=30, 
        title='Ride Distance Distribution',
        labels={'Ride_Distance': 'Distance (km)'}
    )
    st.plotly_chart(fig)


# Canceled Rides by Driver (Count Plot)
def plot_canceled_rides_by_driver(data):
    fig = px.bar(
        data_frame=data,
        x='Canceled_Rides_by_Driver',
        title='Canceled Rides by Driver',
        labels={'Canceled_Rides_by_Driver': 'Canceled Rides by Driver'},
        color='Canceled_Rides_by_Driver',
        color_continuous_scale='Viridis'
    )

    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)


# Canceled Rides by Customer (Count Plot)
def plot_canceled_rides_by_customer(data):
    fig = px.bar(
        data_frame=data,
        x='Canceled_Rides_by_Customer',
        title='Canceled Rides by Customer',
        labels={'Canceled_Rides_by_Customer': 'Canceled Rides by Customer'},
        color='Canceled_Rides_by_Customer',
        color_continuous_scale='Viridis'
    )

    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)







# Streamlit Part
st.set_page_config(page_title="Ola Ride Insights", page_icon="ola_logo.png", layout="wide", initial_sidebar_state="expanded")


# Header Section
#st.title(" Ola Ride Insights Dashboard")
col1, col2 = st.columns([2,14])

with col1:
    st.image("ola_logo.png", width=100)

with col2:
    st.title("Ola Ride Insights Dashboard")
st.write("Explore key insights into Ola's ride-sharing data.")

# Sidebar Menu
with st.sidebar:
    st.write("## Writer: Aamir Sohail")
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "EDA", "SQL Queries", "Power BI Report", "About"],
        icons=["house", "bar-chart-line","database", "bar-chart", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px"},
            "icon": {"color": "white", "font-size": "22px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "center",
                "padding": "12px",
                "color": "white",
            },
        },
    )


# Content Based on Menu Selection
if selected == "Home":
    st.subheader("Welcome to Ola Ride Insights")
    st.write(
        "This dashboard provides an interactive exploration of Ola's ride-sharing data. "
        "Use the navigation menu to explore analytics and learn more about the project."
    )

elif selected == "EDA":
    
    st.subheader("Exporatory Data Analysis Report")

    data = load_data()   
    st.markdown("### 📊 Rides Per Day Distribution")
    plot_rides_per_day_distribution(data)
  
    
    # Booking Status Pie Chart
    st.markdown("### 📊 Booking Status Distribution")
    plot_booking_status_pie_chart(data)

    # Bookings by Day of Week
    st.markdown("### 📊 Bookings by Day of the Week")
    plot_bookings_by_day(data)

    # Payment Method Distribution
    st.markdown("### 📊 Payment Method Distribution")
    plot_payment_method_pie_chart(data)


    # Customer vs Driver Ratings Distribution
    st.markdown("### 📊 Customer vs Driver Ratings Distribution")
    plot_ratings_distribution(data)

    # Incomplete Rides Pie Chart
    st.markdown("### 📊 Incomplete Rides Distribution")
    plot_incomplete_rides_pie_chart(data)

    # Incomplete Rides Reasons
    st.markdown("### 📊 Incomplete Rides Reasons")
    plot_incomplete_rides_reasons(data)

    # Ride Distance Distribution
    st.markdown("### 📊 Distribution of Ride Distance")
    plot_ride_distance_distribution(data)

    # Canceled Rides by Driver
    st.markdown("### 📊 Canceled Rides by Driver")
    plot_canceled_rides_by_driver(data)

    # Canceled Rides by Customer
    st.markdown("### 📊 Canceled Rides by Customer")
    plot_canceled_rides_by_customer(data)


elif selected == "SQL Queries":
    st.subheader("SQL Questions and Visualizations")
    selected_query = st.selectbox(
        "Select SQL Questions", 
        [
            "1. Retrieve all successful bookings", 
            "2. Find the average ride distance for each vehicle type", 
            "3. Get the total number of cancelled rides by customers", 
            "4. List the top 5 customers who booked the highest number of rides",
            "5. Get the number of rides cancelled by drivers due to personal and car-related issues",
            "6. Find the maximum and minimum driver ratings for Prime Sedan bookings",
            "7. Retrieve all rides where payment was made using UPI",
            "8. Find the average customer rating per vehicle type",
            "9. Calculate the total booking value of rides completed successfully",
            "10. List all incomplete rides along with the reason"
            
        ]
    )

    data = load_data()
    if selected_query == "1. Retrieve all successful bookings":
        # Query #1
        st.markdown("###  Query #1: Retrieve all successful bookings")
        st.code("SELECT * FROM ola_rides WHERE Booking_Status = 'Success';", language='sql')

        # Filter DataFrame based on SQL logic
        success_data = data[data['Booking_Status'] == 'Success']

        # Show result table
        st.dataframe(success_data)

        # Plot: Distribution of Successful Rides by Day
        st.markdown("####  Successful Bookings Over Time")
        success_data['Date'] = pd.to_datetime(success_data['Date'])
        success_counts = success_data['Date'].value_counts().sort_index()

        fig = px.line(
            x=success_counts.index,
            y=success_counts.values,
            labels={'x': 'Date', 'y': 'Number of Successful Bookings'},
            title='Successful Bookings Per Day'
        )
        st.plotly_chart(fig)


    if selected_query == "2. Find the average ride distance for each vehicle type":
        st.markdown("###  Query #2: Avg Ride Distance by Vehicle Type")
        st.code("SELECT Vehicle_Type, AVG(Ride_Distance) AS avg_distance FROM ola_rides GROUP BY Vehicle_Type;", language='sql')

        result = data.groupby('Vehicle_Type')['Ride_Distance'].mean().reset_index()
        result.columns = ['Vehicle_Type', 'avg_distance']
        st.dataframe(result)

        fig = px.bar(result, x='Vehicle_Type', y='avg_distance', title="Avg Ride Distance per Vehicle Type")
        st.plotly_chart(fig)


    if selected_query == "3. Get the total number of cancelled rides by customers":
        st.markdown("###  Query #3: Total Rides Cancelled by Customers")
        st.code("SELECT COUNT(*) FROM ola_rides WHERE Booking_Status = 'canceled by Customer';", language='sql')

        total = data[data['Booking_Status'].str.lower() == 'canceled by customer'].shape[0]
        st.metric("Cancelled by Customer", total)


    if selected_query == "4. List the top 5 customers who booked the highest number of rides":
        st.markdown("###  Query #4: Top 5 Customers by Rides")
        st.code("SELECT Customer_ID, COUNT(Booking_ID) AS total_rides FROM ola_rides GROUP BY Customer_ID ORDER BY total_rides DESC LIMIT 5;", language='sql')

        result = data.groupby('Customer_ID')['Booking_ID'].count().reset_index().sort_values(by='Booking_ID', ascending=False).head(5)
        result.columns = ['Customer_ID', 'total_rides']
        st.dataframe(result)

        fig = px.bar(result, x='Customer_ID', y='total_rides', title="Top 5 Customers by Ride Count")
        st.plotly_chart(fig)


    if selected_query == "5. Get the number of rides cancelled by drivers due to personal and car-related issues":
        st.markdown("###  Query #5: Rides Cancelled by Driver (Personal & Car Issues)")
        st.code("""SELECT COUNT(*) FROM ola_rides WHERE Canceled_Rides_by_Driver = "Personal & Car related issue";""", language='sql')

        count = data[data['Canceled_Rides_by_Driver'].str.lower() == 'personal & car related issue'].shape[0]
        st.metric("Driver Cancellations (Personal & Car)", count)


    if selected_query == "6. Find the maximum and minimum driver ratings for Prime Sedan bookings":
        st.markdown("###  Query #6: Max/Min Driver Ratings (Prime Sedan)")
        st.code("SELECT MAX(Driver_Ratings), MIN(Driver_Ratings) FROM ola_rides WHERE Vehicle_Type = 'Prime Sedan';", language='sql')

        prime_data = data[data['Vehicle_Type'] == 'Prime Sedan']
        st.metric("Max Rating", prime_data['Driver_Ratings'].max())
        st.metric("Min Rating", prime_data['Driver_Ratings'].min())



    if selected_query == "7. Retrieve all rides where payment was made using UPI":
        st.markdown("###  Query #7: Rides Paid Using UPI")
        st.code("SELECT * FROM ola_rides WHERE Payment_Method = 'UPI';", language='sql')

        result = data[data['Payment_Method'] == 'UPI']
        st.dataframe(result)

        fig = px.histogram(result, x='Ride_Distance', nbins=20, title='Ride Distance Distribution (UPI)')
        st.plotly_chart(fig)


    if selected_query == "8. Find the average customer rating per vehicle type":
        st.markdown("###  Query #8: Avg Customer Rating per Vehicle Type")
        st.code("SELECT Vehicle_Type, AVG(Customer_Rating) AS avg_customer_rating FROM ola_rides GROUP BY Vehicle_Type;", language='sql')

        result = data.groupby('Vehicle_Type')['Customer_Rating'].mean().reset_index()
        result.columns = ['Vehicle_Type', 'avg_customer_rating']
        st.dataframe(result)

        fig = px.bar(result, x='Vehicle_Type', y='avg_customer_rating', title="Avg Customer Rating by Vehicle Type")
        st.plotly_chart(fig)


    if selected_query == "9. Calculate the total booking value of rides completed successfully":
        st.markdown("###  Query #9: Total Booking Value (Successful)")
        st.code("SELECT SUM(Booking_Value) AS total_successful_rides_value FROM ola_rides WHERE Booking_Status = 'Success';", language='sql')

        total = data[data['Booking_Status'] == 'Success']['Booking_Value'].sum()
        st.metric("Total Value", f"₹ {total:,.2f}")


    if selected_query == "10. List all incomplete rides along with the reason":
        st.markdown("###  Query #10: Incomplete Rides and Reasons")
        st.code("SELECT Booking_ID, Incomplete_Rides_Reason FROM ola_rides WHERE Incomplete_Rides = 'Yes';", language='sql')

        result = data[data['Incomplete_Rides'].astype(str).str.lower() == 'yes'][['Booking_ID', 'Incomplete_Rides_Reason']]
        st.dataframe(result)

        reason_counts = result['Incomplete_Rides_Reason'].value_counts().reset_index()
        reason_counts.columns = ['Reason', 'Count']
        fig = px.bar(reason_counts, x='Reason', y='Count', title='Reasons for Incomplete Rides')
        st.plotly_chart(fig)



elif selected == "Power BI Report":
    st.subheader("📊 Embedded Power BI Dashboard")
    powerbi_url = "https://app.powerbi.com/view?r=YOUR_EMBED_URL"
    st.components.v1.iframe(powerbi_url, width=1100, height=700)


elif selected == "About":
    st.subheader("About the Project")
    st.write(
        "This project focuses on providing insights into Ola's ride-sharing business using data analytics. "
        "You can explore user behavior, ride trends, and much more through this interactive dashboard."
    )
    st.write("Developer: Aamir Sohail")
    st.write("GitHub Repository: [Click Here](https://github.com/your-repo-link)")
