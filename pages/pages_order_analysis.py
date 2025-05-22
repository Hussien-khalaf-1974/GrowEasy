# import streamlit as st
# import pandas as pd
# from statsmodels.tsa.arima.model import ARIMA
# import plotly.express as px
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors
# from reportlab.platypus.tables import TableStyle
# import io
# from datetime import datetime

# st.title("Order Analysis")

# if 'data' not in st.session_state:
#     st.error("Please upload an Excel file on the main page.")
# else:
#     orders = st.session_state['data']['Orders']
#     customers = st.session_state['data']['Customers']
    
#     # Key Present Metrics
#     # Total number of orders
#     total_orders = len(orders)
    
#     # Order status distribution
#     order_status_dist = orders['status'].value_counts()
    
#     # Daily/weekly/monthly order trends
#     orders['order_date'] = pd.to_datetime(orders['order_date'])
#     daily_orders = orders.resample('D', on='order_date')['id'].count()
#     weekly_orders = orders.resample('W', on='order_date')['id'].count()
#     monthly_orders = orders.resample('M', on='order_date')['id'].count()
    
#     # Average order value
#     avg_order_value = orders['total_amount'].mean()
    
#     # Future-Oriented Insights
#     # Forecasted order volume
#     model = ARIMA(weekly_orders, order=(1, 1, 1))
#     fit = model.fit()
#     forecast = fit.forecast(steps=4)
#     forecast_df = pd.DataFrame({'Week': forecast.index, 'Predicted Orders': forecast.values})
    
#     # Cancelled order trends
#     cancelled_orders = orders[orders['status'].str.lower() == 'cancelled']
#     cancelled_trends = cancelled_orders.resample('M', on='order_date')['id'].count().reset_index(name='cancelled_count')
    
#     # High-value customers or periods
#     high_value_customers = orders.groupby('customer_id')['total_amount'].sum().reset_index()
#     high_value_customers = high_value_customers.merge(customers[['id', 'email']], left_on='customer_id', right_on='id')
#     high_value_customers = high_value_customers.sort_values('total_amount', ascending=False).head(5)
#     high_value_periods = orders.resample('W', on='order_date')['total_amount'].sum().sort_values(ascending=False).head(3)
    
#     # Display Metrics
#     st.subheader("Key Present Metrics")
#     col1, col2 = st.columns(2)
#     col1.metric("Total Orders", total_orders)
#     col2.metric("Average Order Value", f"${avg_order_value:.2f}")
    
#     st.subheader("Order Status Distribution")
#     st.write(order_status_dist)
    
#     st.subheader("Order Trends")
#     fig_daily = px.line(daily_orders, title="Daily Order Trends")
#     fig_weekly = px.line(weekly_orders, title="Weekly Order Trends")
#     fig_monthly = px.line(monthly_orders, title="Monthly Order Trends")
#     st.plotly_chart(fig_daily)
#     st.plotly_chart(fig_weekly)
#     st.plotly_chart(fig_monthly)
    
#     # Future Insights
#     st.subheader("Forecasted Order Volume")
#     fig_forecast = px.line(weekly_orders, title="Weekly Order Trends with Forecast")
#     fig_forecast.add_scatter(x=forecast_df['Week'], y=forecast_df['Predicted Orders'], mode='lines', name='Forecast')
#     st.plotly_chart(fig_forecast)
    
#     st.subheader("Cancelled Order Trends")
#     st.dataframe(cancelled_trends)
    
#     st.subheader("High-Value Customers")
#     st.dataframe(high_value_customers[['email', 'total_amount']])
    
#     st.subheader("High-Value Periods")
#     st.write(high_value_periods)
    
#     recommendation = f"Increase marketing during high-value periods and target {len(high_value_customers)} high-value customers."
#     st.write(f"Recommendation: {recommendation}")
    
#     # PDF Download Section
#     pdf_buffer = io.BytesIO()
#     doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
#     styles = getSampleStyleSheet()
#     elements = [
#         Paragraph("Order Analysis Report", styles['Title']),
#         Paragraph("Key Present Metrics", styles['Heading2']),
#         Spacer(1, 12),
#         Paragraph(f"Author: GrowEasy Platform", styles['Normal']),
#         Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
#         Spacer(1, 12),
#     ]
    
#     # Add Metrics Table
#     data = [['Metric', 'Value']]
#     data.append(['Total Orders', str(total_orders)])
#     data.append(['Average Order Value', f"${avg_order_value:.2f}"])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add Order Status Distribution
#     elements.append(Paragraph("Order Status Distribution", styles['Heading2']))
#     data = [['Status', 'Count']]
#     for status, count in order_status_dist.items():
#         data.append([status, str(count)])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add Cancelled Order Trends
#     if not cancelled_trends.empty:
#         elements.append(Paragraph("Cancelled Order Trends", styles['Heading2']))
#         data = [['Month', 'Cancelled Orders']]
#         for _, row in cancelled_trends.iterrows():
#             data.append([row['order_date'].strftime('%Y-%m-%d'), str(row['cancelled_count'])])
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ]))
#         elements.append(table)
#         elements.append(Spacer(1, 12))
    
#     # Add High-Value Customers
#     elements.append(Paragraph("High-Value Customers", styles['Heading2']))
#     data = [['Email', 'Total Spent']]
#     for _, row in high_value_customers.iterrows():
#         data.append([row['email'], f"${row['total_amount']:.2f}"])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add High-Value Periods
#     elements.append(Paragraph("High-Value Periods", styles['Heading2']))
#     data = [['Week', 'Total Revenue']]
#     for week, revenue in high_value_periods.items():
#         data.append([week.strftime('%Y-%m-%d'), f"${revenue:.2f}"])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     elements.append(Paragraph("Recommendation", styles['Heading2']))
#     elements.append(Paragraph(recommendation, styles['Normal']))
    
#     try:
#         doc.build(elements)
#         pdf_buffer.seek(0, 2)
#         buffer_size = pdf_buffer.tell()
#         st.write(f"Debug: PDF buffer size is {buffer_size} bytes")
#         pdf_buffer.seek(0)
#         st.download_button(
#             label="Download Order Analysis Report",
#             data=pdf_buffer.getvalue(),
#             file_name="Order_Analysis_Report.pdf",
#             mime="application/pdf"
#         )
#     except Exception as e:
#         st.error(f"Error generating PDF: {str(e)}. Please ensure reportlab is installed.")










import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.tables import TableStyle
import io
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(layout="wide", page_title="GrowEasy: Order Analysis")

# CSS styling
st.markdown(
    """
    <style>
    .title {
        animation: fadeIn 1s ease-in-out;
        color: #4f627c;
        font-size: 3.5em;
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin: 30px 0;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .stButton>button {
        background-color: #4CAF50;
        color: #d3d3d3;
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        border: 1px solid #2c3e50;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        margin: 10px 0;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.03);
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
    }
    .stExpander {
        border-radius: 8px;
        background-color: #1f2a44;
        color: #d3d3d3;
        border: 1px solid #2c3e50;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
        margin: 15px 0;
        padding: 10px;
    }
    .stMultiSelect label {
        color: #000000;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        margin-top: 15px;
    }
    .metric {
        animation: fadeIn 1.2s ease-in-out;
        background-color: #141c30;
        color: #d3d3d3;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2c3e50;
        font-family: 'Arial', sans-serif;
        margin: 10px 0;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1f2a44;
        color: #d3d3d3;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        margin-right: 10px;
        transition: all 0.3s ease;
        font-family: 'Arial', sans-serif;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #141c30;
        color: #000000;
        border-bottom: 2px solid #4CAF50;
    }
    .section-spacer {
        margin: 20px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Animated title
st.markdown('<div class="title">Order Analysis</div>', unsafe_allow_html=True)

# Check for data
if 'data' not in st.session_state or st.session_state['data'] is None:
    st.error("Please upload an Excel file on the main page.")
else:
    try:
        # Validate required columns
        required_columns = {'Orders': ['id', 'order_date', 'status', 'total_amount', 'customer_id'], 'Customers': ['id', 'email']}
        for sheet, cols in required_columns.items():
            if sheet not in st.session_state['data']:
                raise ValueError(f"Missing required sheet: {sheet}")
            missing_cols = [col for col in cols if col not in st.session_state['data'][sheet].columns]
            if missing_cols:
                raise ValueError(f"Missing columns in {sheet}: {', '.join(missing_cols)}")
        
        orders = st.session_state['data']['Orders']
        customers = st.session_state['data']['Customers']
        
        # Key Present Metrics
        total_orders = len(orders)
        order_status_dist = orders['status'].value_counts()
        orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
        if orders['order_date'].isna().all():
            raise ValueError("Invalid or missing 'order_date' values in Orders data")
        daily_orders = orders.resample('D', on='order_date')['id'].count()
        weekly_orders = orders.resample('W', on='order_date')['id'].count()
        monthly_orders = orders.resample('M', on='order_date')['id'].count()
        avg_order_value = orders['total_amount'].mean()
        
        # Future-Oriented Insights
        try:
            model = ARIMA(weekly_orders, order=(1, 1, 1))
            fit = model.fit()
            forecast = fit.forecast(steps=4)
            forecast_df = pd.DataFrame({'Week': forecast.index, 'Predicted Orders': forecast.values})
        except Exception as e:
            st.error(f"Error in ARIMA forecast: {e}")
            forecast_df = pd.DataFrame()
        
        cancelled_orders = orders[orders['status'].str.lower() == 'cancelled']
        cancelled_trends = cancelled_orders.resample('M', on='order_date')['id'].count().reset_index(name='cancelled_count')
        high_value_customers = orders.groupby('customer_id')['total_amount'].sum().reset_index()
        high_value_customers = high_value_customers.merge(customers[['id', 'email']], left_on='customer_id', right_on='id')
        high_value_customers = high_value_customers.sort_values('total_amount', ascending=False).head(5)
        high_value_periods = orders.resample('W', on='order_date')['total_amount'].sum().sort_values(ascending=False).head(3)
        
        # Sidebar filters
        st.sidebar.subheader("Filter Options")
        status_options = orders['status'].dropna().unique()
        status_filter = st.sidebar.multiselect(
            "Select Order Status",
            options=status_options,
            default=status_options,
            key="status_multiselect"
        )
        date_min = orders['order_date'].min().date() if not orders['order_date'].empty else datetime.today().date()
        date_max = orders['order_date'].max().date() if not orders['order_date'].empty else datetime.today().date()
        date_filter = st.sidebar.date_input(
            "Select Date Range",
            value=(date_min, date_max),
            min_value=date_min,
            max_value=date_max,
            key="date_range"
        )
        st.sidebar.button("Clear Filters", key="clear_filters", on_click=lambda: st.session_state.update(
            status_multiselect=status_options, date_range=(date_min, date_max)))
        
        # Apply filters
        filtered_orders = orders
        if status_filter:
            filtered_orders = filtered_orders[filtered_orders['status'].isin(status_filter)]
        if len(date_filter) == 2:
            start_date, end_date = date_filter
            filtered_orders = filtered_orders[(filtered_orders['order_date'].dt.date >= start_date) & (filtered_orders['order_date'].dt.date <= end_date)]
        
        # Recalculate metrics for filtered data
        total_filtered_orders = len(filtered_orders)
        filtered_order_status_dist = filtered_orders['status'].value_counts()
        filtered_avg_order_value = filtered_orders['total_amount'].mean() if 'total_amount' in filtered_orders.columns else 0
        filtered_daily_orders = filtered_orders.resample('D', on='order_date')['id'].count()
        filtered_weekly_orders = filtered_orders.resample('W', on='order_date')['id'].count()
        filtered_monthly_orders = filtered_orders.resample('M', on='order_date')['id'].count()
        filtered_cancelled_orders = filtered_orders[filtered_orders['status'].str.lower() == 'cancelled']
        filtered_cancelled_trends = filtered_cancelled_orders.resample('M', on='order_date')['id'].count().reset_index(name='cancelled_count')
        filtered_high_value_customers = filtered_orders.groupby('customer_id')['total_amount'].sum().reset_index()
        filtered_high_value_customers = filtered_high_value_customers.merge(customers[['id', 'email']], left_on='customer_id', right_on='id').sort_values('total_amount', ascending=False).head(5)
        filtered_high_value_periods = filtered_orders.resample('W', on='order_date')['total_amount'].sum().sort_values(ascending=False).head(3)
        
        st.write(f"Showing {total_filtered_orders} of {total_orders} orders after filtering.")
        
        # Tabs
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Present Metrics", "Visual  Visualizations", "Future Insights"])
        
        with tab1:
            st.subheader("Key Present Metrics")
            col1, col2 = st.columns(2)
            col1.markdown(f'<div class="metric">Total Orders: {total_filtered_orders}</div>', unsafe_allow_html=True)
            col2.markdown(f'<div class="metric">Average Order Value: ${filtered_avg_order_value:.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            
            with st.expander("Order Status Distribution"):
                if not filtered_order_status_dist.empty:
                    st.dataframe(filtered_order_status_dist.reset_index().rename(columns={'index': 'Status', 'status': 'Count'}), use_container_width=True)
                else:
                    st.write("No order status data available.")
        
        with tab2:
            st.subheader("Order Trends")
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            trend_option = st.selectbox("Select Trend Period", ["Daily", "Weekly", "Monthly"], key="trend_select")
            if trend_option == "Daily":
                data = filtered_daily_orders
                title = "Daily Order Trends"
            elif trend_option == "Weekly":
                data = filtered_weekly_orders
                title = "Weekly Order Trends"
            else:
                data = filtered_monthly_orders
                title = "Monthly Order Trends"
            if not data.empty:
                fig = px.line(data, title=title, color_discrete_sequence=['#4CAF50'])
                fig.update_traces(mode='lines+markers', hovertemplate='Date: %{x}<br>Orders: %{y}')
                fig.update_layout(xaxis_title="Date", yaxis_title="Orders")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No order trend data available.")
        
        with tab3:
            st.subheader("Future Insights")
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            with st.expander("Forecasted Order Volume"):
                if not forecast_df.empty:
                    fig_forecast = px.line(weekly_orders, title="Weekly Order Trends with Forecast", color_discrete_sequence=['#4CAF50'])
                    fig_forecast.add_scatter(x=forecast_df['Week'], y=forecast_df['Predicted Orders'], mode='lines', name='Forecast', line=dict(color='#FF6F61'))
                    fig_forecast.update_traces(hovertemplate='Date: %{x}<br>Orders: %{y}')
                    fig_forecast.update_layout(xaxis_title="Date", yaxis_title="Orders")
                    st.plotly_chart(fig_forecast, use_container_width=True)
                else:
                    st.write("Forecast unavailable due to data issues.")
            
            with st.expander("Cancelled Order Trends"):
                if not filtered_cancelled_trends.empty:
                    st.dataframe(filtered_cancelled_trends, use_container_width=True)
                else:
                    st.write("No cancelled orders identified.")
            
            with st.expander("High-Value Customers"):
                if not filtered_high_value_customers.empty:
                    st.dataframe(filtered_high_value_customers[['email', 'total_amount']], use_container_width=True)
                else:
                    st.write("No high-value customers identified.")
            
            with st.expander("High-Value Periods"):
                if not filtered_high_value_periods.empty:
                    st.dataframe(filtered_high_value_periods.reset_index().rename(columns={'order_date': 'Week', 'total_amount': 'Total Revenue'}), use_container_width=True)
                else:
                    st.write("No high-value periods identified.")
            
            recommendation = f"Increase marketing during high-value periods and target {len(filtered_high_value_customers)} high-value customers."
            st.markdown(f"**Recommendation**: {recommendation}")
        
        # PDF Download
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        with st.spinner("Generating PDF Report..."):
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = [
                Paragraph("Order Analysis Report", styles['Title']),
                Paragraph("Key Present Metrics", styles['Heading2']),
                Spacer(1, 20),
                Paragraph(f"Author: GrowEasy Platform", styles['Normal']),
                Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
                Spacer(1, 20),
            ]
            
            # Metrics Table
            data = [['Metric', 'Value']]
            data.append(['Total Orders', str(total_filtered_orders)])
            data.append(['Average Order Value', f"${filtered_avg_order_value:.2f}"])
            table = Table(data)
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 20))
            
            # Order Status Distribution
            if not filtered_order_status_dist.empty:
                elements.append(Paragraph("Order Status Distribution", styles['Heading2']))
                data = [['Status', 'Count']]
                for status, count in filtered_order_status_dist.items():
                    data.append([status, str(count)])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # Cancelled Order Trends
            if not filtered_cancelled_trends.empty:
                elements.append(Paragraph("Cancelled Order Trends", styles['Heading2']))
                data = [['Month', 'Cancelled Orders']]
                for _, row in filtered_cancelled_trends.iterrows():
                    data.append([row['order_date'].strftime('%Y-%m-%d'), str(row['cancelled_count'])])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # High-Value Customers
            if not filtered_high_value_customers.empty:
                elements.append(Paragraph("High-Value Customers", styles['Heading2']))
                data = [['Email', 'Total Spent']]
                for _, row in filtered_high_value_customers.iterrows():
                    data.append([row['email'], f"${row['total_amount']:.2f}"])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # High-Value Periods
            if not filtered_high_value_periods.empty:
                elements.append(Paragraph("High-Value Periods", styles['Heading2']))
                data = [['Week', 'Total Revenue']]
                for week, revenue in filtered_high_value_periods.items():
                    data.append([week.strftime('%Y-%m-%d'), f"${revenue:.2f}"])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            elements.append(Paragraph("Recommendation", styles['Heading2']))
            elements.append(Paragraph(recommendation, styles['Normal']))
            
            try:
                doc.build(elements)
                pdf_buffer.seek(0)
                st.download_button(
                    label="Download Order Analysis Report",
                    data=pdf_buffer.getvalue(),
                    file_name="Order_Analysis_Report.pdf",
                    mime="application/pdf",
                    key="download_pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
    
    except ValueError as ve:
        st.error(f"Data validation error: {ve}")
    except Exception as e:
        st.error(f"Error processing data: {e}")