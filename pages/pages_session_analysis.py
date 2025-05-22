# import streamlit as st
# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler
# import plotly.express as px
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors
# from reportlab.platypus.tables import TableStyle
# import io
# from datetime import datetime

# st.title("Session Analysis")

# if 'data' not in st.session_state:
#     st.error("Please upload an Excel file on the main page.")
# else:
#     sessions = st.session_state['data']['Customer_Sessions']
#     orders = st.session_state['data']['Orders']
    
#     # Key Present Metrics
#     # Number of sessions per customer
#     sessions_per_customer = sessions.groupby('customer_id').size().reset_index(name='session_count')
    
#     # Average session duration
#     sessions['duration'] = (pd.to_datetime(sessions['session_end']) - pd.to_datetime(sessions['session_start'])).dt.total_seconds() / 60
#     avg_duration = sessions['duration'].mean()
    
#     # Sessions per day/week
#     sessions['session_start'] = pd.to_datetime(sessions['session_start'])
#     daily_sessions = sessions.resample('D', on='session_start')['id'].count()
#     weekly_sessions = sessions.resample('W', on='session_start')['id'].count()
    
#     # Future-Oriented Insights
#     # Predict customer activity
#     sessions['high_engagement'] = (sessions['duration'] > 5).astype(int)
#     features = ['duration']
#     X = sessions[features]
#     y = sessions['high_engagement']
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(X)
#     model = RandomForestClassifier(n_estimators=100)
#     model.fit(X_scaled, y)
#     sessions['engagement_probability'] = model.predict_proba(X_scaled)[:, 1]
#     recent_sessions = sessions[sessions['session_start'] > datetime.now() - pd.Timedelta(days=30)]
#     likely_to_return = recent_sessions.groupby('customer_id')['engagement_probability'].mean().reset_index()
#     likely_to_return = likely_to_return[likely_to_return['engagement_probability'] > 0.7]
    
#     # Correlate session activity with orders (conversion rates)
#     customer_orders = orders.groupby('customer_id')['id'].count().reset_index(name='order_count')
#     conversion_data = sessions_per_customer.merge(customer_orders, on='customer_id', how='left').fillna(0)
#     conversion_data['conversion_rate'] = conversion_data['order_count'] / conversion_data['session_count']
#     high_conversion = conversion_data[conversion_data['conversion_rate'] > conversion_data['conversion_rate'].mean()]
    
#     # Identify peak browsing times
#     sessions['hour'] = sessions['session_start'].dt.hour
#     peak_hours = sessions.groupby('hour')['id'].count().sort_values(ascending=False).head(3)
    
#     # Display Metrics
#     st.subheader("Key Present Metrics")
#     col1, col2 = st.columns(2)
#     col1.metric("Average Session Duration", f"{avg_duration:.2f} minutes")
#     col2.metric("Total Sessions", len(sessions))
    
#     st.subheader("Sessions per Customer")
#     st.dataframe(sessions_per_customer)
    
#     st.subheader("Session Trends")
#     fig_daily = px.line(daily_sessions, title="Daily Sessions")
#     fig_weekly = px.line(weekly_sessions, title="Weekly Sessions")
#     st.plotly_chart(fig_daily)
#     st.plotly_chart(fig_weekly)
    
#     # Future Insights
#     st.subheader("Customers Likely to Return Soon")
#     st.dataframe(likely_to_return)
    
#     st.subheader("High Conversion Customers")
#     st.dataframe(high_conversion[['customer_id', 'session_count', 'order_count', 'conversion_rate']])
    
#     st.subheader("Peak Browsing Times")
#     st.write(peak_hours)
    
#     recommendation = f"Optimize support availability during peak hours and target {len(high_conversion)} high-conversion customers."
#     st.write(f"Recommendation: {recommendation}")
    
#     # PDF Download Section
#     pdf_buffer = io.BytesIO()
#     doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
#     styles = getSampleStyleSheet()
#     elements = [
#         Paragraph("Session Analysis Report", styles['Title']),
#         Paragraph("Key Present Metrics", styles['Heading2']),
#         Spacer(1, 12),
#         Paragraph(f"Author: GrowEasy Platform", styles['Normal']),
#         Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
#         Spacer(1, 12),
#     ]
    
#     # Add Metrics Table
#     data = [['Metric', 'Value']]
#     data.append(['Total Sessions', str(len(sessions))])
#     data.append(['Average Session Duration', f"{avg_duration:.2f} minutes"])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add Sessions per Customer (top 5)
#     elements.append(Paragraph("Sessions per Customer (Top 5)", styles['Heading2']))
#     data = [['Customer ID', 'Session Count']]
#     for _, row in sessions_per_customer.head(5).iterrows():
#         data.append([str(row['customer_id']), str(row['session_count'])])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add Likely to Return
#     if not likely_to_return.empty:
#         elements.append(Paragraph("Customers Likely to Return Soon", styles['Heading2']))
#         data = [['Customer ID', 'Engagement Probability']]
#         for _, row in likely_to_return.iterrows():
#             data.append([str(row['customer_id']), f"{row['engagement_probability']*100:.1f}%"])
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ]))
#         elements.append(table)
#         elements.append(Spacer(1, 12))
    
#     # Add High Conversion Customers
#     if not high_conversion.empty:
#         elements.append(Paragraph("High Conversion Customers", styles['Heading2']))
#         data = [['Customer ID', 'Session Count', 'Order Count', 'Conversion Rate']]
#         for _, row in high_conversion.iterrows():
#             data.append([str(row['customer_id']), str(row['session_count']), str(row['order_count']), f"{row['conversion_rate']:.2f}"])
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ]))
#         elements.append(table)
#         elements.append(Spacer(1, 12))
    
#     # Add Peak Browsing Times
#     elements.append(Paragraph("Peak Browsing Times", styles['Heading2']))
#     data = [['Hour', 'Session Count']]
#     for hour, count in peak_hours.items():
#         data.append([f"{hour}:00", str(count)])
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
#             label="Download Session Analysis Report",
#             data=pdf_buffer.getvalue(),
#             file_name="Session_Analysis_Report.pdf",
#             mime="application/pdf"
#         )
#     except Exception as e:
#         st.error(f"Error generating PDF: {str(e)}. Please ensure reportlab is installed.")



import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.tables import TableStyle
import io
from datetime import datetime, timedelta

# Set page config for professional layout
st.set_page_config(layout="wide", page_title="GrowEasy: Session Analysis")

# Professional CSS with harmonious dark palette
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
    .stDateInput label, .stSelectbox label {
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
st.markdown('<div class="title">Session Analysis</div>', unsafe_allow_html=True)

# Check for data
if 'data' not in st.session_state or st.session_state['data'] is None:
    st.error("Please upload an Excel file on the main page.")
else:
    try:
        # Load and validate data
        sessions = st.session_state['data']['Customer_Sessions'].rename(columns={'id': 'session_id'})
        orders = st.session_state['data']['Orders'].rename(columns={'id': 'order_id'})
        required_cols = ['session_id', 'customer_id', 'session_start', 'session_end']
        missing_cols = [col for col in required_cols if col not in sessions.columns]
        if missing_cols:
            st.error(f"Missing required columns in Customer_Sessions: {', '.join(missing_cols)}")
            st.stop()
        try:
            sessions['session_start'] = pd.to_datetime(sessions['session_start'], errors='coerce')
            sessions['session_end'] = pd.to_datetime(sessions['session_end'], errors='coerce')
            if sessions['session_start'].isnull().any() or sessions['session_end'].isnull().any():
                st.error("Invalid datetime format in session_start or session_end.")
                st.stop()
        except Exception as e:
            st.error(f"Error parsing session dates: {e}")
            st.stop()

        # Sidebar filters
        st.sidebar.subheader("Filter Options")
        date_start, date_end = st.sidebar.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            min_value=datetime(2020, 1, 1),
            max_value=datetime.now(),
            key="date_range"
        )
        engagement_filter = st.sidebar.selectbox(
            "Engagement Level",
            options=["All", "High (>70%)", "Medium (30-70%)", "Low (<30%)"],
            help="Filter by engagement probability.",
            key="engagement_select"
        )
        st.sidebar.button("Clear Filters", key="clear_filters", on_click=lambda: st.session_state.update(
            date_range=(datetime.now() - timedelta(days=30), datetime.now()), engagement_select="All"))

        # Apply date filter
        start_date = pd.to_datetime(date_start)
        end_date = pd.to_datetime(date_end) + pd.Timedelta(days=1)
        filtered_sessions = sessions[
            (sessions['session_start'] >= start_date) & (sessions['session_start'] < end_date)
        ]

        # Key Metrics
        sessions_per_customer = filtered_sessions.groupby('customer_id').size().reset_index(name='session_count')
        filtered_sessions['duration'] = (filtered_sessions['session_end'] - filtered_sessions['session_start']).dt.total_seconds() / 60
        avg_duration = filtered_sessions['duration'].mean() if not filtered_sessions.empty else 0
        total_sessions = len(filtered_sessions)
        daily_sessions = filtered_sessions.resample('D', on='session_start')['session_id'].count()
        weekly_sessions = filtered_sessions.resample('W', on='session_start')['session_id'].count()
        filtered_sessions['hour'] = filtered_sessions['session_start'].dt.hour
        peak_hours = filtered_sessions.groupby('hour')['session_id'].count().reset_index(name='session_count').sort_values('session_count', ascending=False).head(3)

        # Predictive Insights
        @st.cache_data
        def train_engagement_model(X, y):
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            model = RandomForestClassifier(n_estimators=100)
            model.fit(X_scaled, y)
            return model, scaler

        filtered_sessions['high_engagement'] = (filtered_sessions['duration'] > 5).astype(int)
        features = ['duration']
        X = filtered_sessions[features]
        y = filtered_sessions['high_engagement']
        if not X.empty and not y.empty:
            model, scaler = train_engagement_model(X, y)
            filtered_sessions['engagement_probability'] = model.predict_proba(scaler.transform(X))[:, 1]
        else:
            filtered_sessions['engagement_probability'] = 0
        recent_sessions = filtered_sessions[filtered_sessions['session_start'] > datetime.now() - pd.Timedelta(days=30)]
        likely_to_return = recent_sessions.groupby('customer_id')['engagement_probability'].mean().reset_index()
        likely_to_return = likely_to_return[likely_to_return['engagement_probability'] > 0.7]

        # Apply engagement filter
        filtered_likely_to_return = likely_to_return
        if engagement_filter != "All":
            if engagement_filter == "High (>70%)":
                filtered_likely_to_return = likely_to_return[likely_to_return['engagement_probability'] > 0.7]
            elif engagement_filter == "Medium (30-70%)":
                filtered_likely_to_return = likely_to_return[(likely_to_return['engagement_probability'] >= 0.3) & (likely_to_return['engagement_probability'] <= 0.7)]
            else:  # Low (<30%)
                filtered_likely_to_return = likely_to_return[likely_to_return['engagement_probability'] < 0.3]

        # Conversion Analysis
        customer_orders = orders.groupby('customer_id')['order_id'].count().reset_index(name='order_count')
        conversion_data = sessions_per_customer.merge(customer_orders, on='customer_id', how='left').fillna(0)
        conversion_data['conversion_rate'] = conversion_data['order_count'] / conversion_data['session_count']
        high_conversion = conversion_data[conversion_data['conversion_rate'] > conversion_data['conversion_rate'].mean()]

        # Tabs for organized display
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Present Metrics", "Visualizations", "Future Insights"])

        with tab1:
            st.subheader("Key Present Metrics")
            col1, col2, col3 = st.columns(3)
            col1.markdown(f'<div class="metric">Total Sessions: {total_sessions}</div>', unsafe_allow_html=True)
            col2.markdown(f'<div class="metric">Avg Duration: {avg_duration:.2f} min</div>', unsafe_allow_html=True)
            col3.markdown(f'<div class="metric">Peak Hour Sessions: {peak_hours["session_count"].max() if not peak_hours.empty else 0}</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

            with st.expander("Sessions per Customer"):
                st.dataframe(sessions_per_customer, use_container_width=True)

        with tab2:
            st.subheader("Session Trends")
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            fig_daily = px.line(daily_sessions, title="Daily Sessions", color_discrete_sequence=['#4CAF50'])
            fig_daily.update_layout(xaxis_title="Date", yaxis_title="Session Count")
            st.plotly_chart(fig_daily, use_container_width=True)
            fig_weekly = px.line(weekly_sessions, title="Weekly Sessions", color_discrete_sequence=['#4CAF50'])
            fig_weekly.update_layout(xaxis_title="Week", yaxis_title="Session Count")
            st.plotly_chart(fig_weekly, use_container_width=True)
            fig_peak = px.bar(peak_hours, x='hour', y='session_count', title="Top 3 Peak Browsing Hours",
                             labels={'hour': 'Hour of Day', 'session_count': 'Session Count'},
                             color_discrete_sequence=['#4CAF50'])
            fig_peak.update_xaxes(tickvals=peak_hours['hour'], ticktext=[f"{h}:00" for h in peak_hours['hour']])
            st.plotly_chart(fig_peak, use_container_width=True)

        with tab3:
            st.subheader("Future Insights")
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            with st.expander("Customers Likely to Return Soon"):
                if not filtered_likely_to_return.empty:
                    st.dataframe(filtered_likely_to_return, use_container_width=True)
                else:
                    st.write("No customers identified as likely to return.")
            with st.expander("High Conversion Customers"):
                if not high_conversion.empty:
                    st.dataframe(high_conversion[['customer_id', 'session_count', 'order_count', 'conversion_rate']], use_container_width=True)
                else:
                    st.write("No high-conversion customers identified.")
            recommendation = f"Optimize support availability during peak hours (e.g., {peak_hours['hour'].iloc[0] if not peak_hours.empty else 'N/A'}:00) and target {len(high_conversion)} high-conversion customers."
            st.markdown(f"**Recommendation**: {recommendation}")

        # PDF Download
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        with st.spinner("Generating PDF Report..."):
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = [
                Paragraph("Session Analysis Report", styles['Title']),
                Paragraph("Key Present Metrics", styles['Heading2']),
                Spacer(1, 20),
                Paragraph("Author: GrowEasy Platform", styles['Normal']),
                Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
                Spacer(1, 20),
            ]

            # Metrics Table
            data = [['Metric', 'Value']]
            data.append(['Total Sessions', str(total_sessions)])
            data.append(['Average Duration', f"{avg_duration:.2f} minutes"])
            data.append(['Peak Hour Sessions', str(peak_hours['session_count'].max() if not peak_hours.empty else 0)])
            table = Table(data)
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 20))

            # Sessions per Customer
            elements.append(Paragraph("Sessions per Customer (Top 5)", styles['Heading2']))
            data = [['Customer ID', 'Session Count']]
            for _, row in sessions_per_customer.head(5).iterrows():
                data.append([str(row['customer_id']), str(row['session_count'])])
            table = Table(data)
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 20))

            # Likely to Return
            if not filtered_likely_to_return.empty:
                elements.append(Paragraph("Customers Likely to Return Soon", styles['Heading2']))
                data = [['Customer ID', 'Engagement Probability']]
                for _, row in filtered_likely_to_return.iterrows():
                    data.append([str(row['customer_id']), f"{row['engagement_probability']*100:.1f}%"])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))

            # High Conversion Customers
            if not high_conversion.empty:
                elements.append(Paragraph("High Conversion Customers", styles['Heading2']))
                data = [['Customer ID', 'Session Count', 'Order Count', 'Conversion Rate']]
                for _, row in high_conversion.iterrows():
                    data.append([str(row['customer_id']), str(row['session_count']), str(row['order_count']), f"{row['conversion_rate']:.2f}"])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))

            # Peak Hours
            elements.append(Paragraph("Peak Browsing Times", styles['Heading2']))
            data = [['Hour', 'Session Count']]
            for _, row in peak_hours.iterrows():
                data.append([f"{row['hour']}:00", str(row['session_count'])])
            table = Table(data)
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 20))

            elements.append(Paragraph("Recommendation", styles['Heading2']))
            elements.append(Paragraph(recommendation, styles['Normal']))

            try:
                doc.build(elements)
                pdf_buffer.seek(0)
                st.download_button(
                    label="Download Session Analysis Report",
                    data=pdf_buffer.getvalue(),
                    file_name="Session_Analysis_Report.pdf",
                    mime="application/pdf",
                    key="download_pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

    except Exception as e:
        st.error(f"Error processing data: {e}")